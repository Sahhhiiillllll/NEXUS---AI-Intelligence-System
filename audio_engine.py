"""
N.A.X.U.S — audio_engine.py
==============================
Async Audio Pipeline:
  - SpeechRecognition with async mic capture
  - Ambient noise calibration
  - pyttsx3 offline TTS (via thread executor)
  - Optional Google Speech API for higher accuracy

Design principle: all blocking calls run in asyncio ThreadPoolExecutor
so the event loop never freezes.
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing             import Callable, Awaitable, Optional

import speech_recognition as sr
import pyttsx3

from logger import get_logger

log = get_logger("audio")

CALIBRATION_DURATION = 1.5   # seconds of ambient noise calibration
PHRASE_TIMEOUT       = 8     # max seconds to wait for a phrase
LISTEN_TIMEOUT       = 3     # seconds before giving up on silence


class TTSEngine:
    """
    Thread-safe pyttsx3 TTS wrapper.
    Runs engine.runAndWait() in a dedicated thread to avoid event-loop blocking.
    """

    def __init__(self):
        self._lock   = threading.Lock()
        self._engine = None
        self._init()

    def _init(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate",   165)
            engine.setProperty("volume", 0.93)

            # Prefer a male English voice
            voices = engine.getProperty("voices")
            preferred = next(
                (v for v in voices if "male" in v.name.lower() and "english" in v.name.lower()),
                voices[0] if voices else None,
            )
            if preferred:
                engine.setProperty("voice", preferred.id)
                log.info(f"TTS voice: {preferred.name}", extra={"event": "tts_init"})

            self._engine = engine
            log.info("pyttsx3 TTS initialized", extra={"event": "tts_init"})
        except Exception as e:
            log.error(f"pyttsx3 init failed: {e}", extra={"event": "tts_error"})

    def speak_blocking(self, text: str):
        """Speak text synchronously (call from thread)."""
        if not self._engine:
            log.warning("TTS engine unavailable — skipping speech")
            return
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as e:
                log.error(f"TTS speak error: {e}", extra={"event": "tts_error"})


class AudioEngine:
    """
    Main audio subsystem.

    Features:
      - Ambient noise calibration on startup
      - Async microphone listen loop (runs in executor)
      - Transcript callback fires into the asyncio event loop
      - async speak_async() for non-blocking TTS
    """

    def __init__(self, on_transcript: Callable[[str], Awaitable[None]] = None):
        self._recognizer     = sr.Recognizer()
        self._tts            = TTSEngine()
        self._executor       = ThreadPoolExecutor(max_workers=4, thread_name_prefix="nexus-audio")
        self._on_transcript  = on_transcript
        self._running        = False
        self._calibrated     = False
        self._loop: asyncio.AbstractEventLoop | None = None

        # Tune recognizer
        self._recognizer.dynamic_energy_threshold = True
        self._recognizer.energy_threshold          = 300
        self._recognizer.pause_threshold           = 0.8

        log.info("AudioEngine created", extra={"event": "audio_init"})

    # ─────────────────────── Noise Calibration ───────────────────────
    def _calibrate(self):
        """Calibrate microphone for ambient noise level (blocking)."""
        try:
            with sr.Microphone() as source:
                log.info(
                    f"Calibrating microphone for {CALIBRATION_DURATION}s...",
                    extra={"event": "calibration_start"}
                )
                self._recognizer.adjust_for_ambient_noise(source, duration=CALIBRATION_DURATION)
                self._calibrated = True
                log.info(
                    f"Calibration complete. Energy threshold: {self._recognizer.energy_threshold:.1f}",
                    extra={"event": "calibration_done", "threshold": self._recognizer.energy_threshold}
                )
        except Exception as e:
            log.error(f"Microphone calibration failed: {e}", extra={"event": "calibration_error"})

    # ─────────────────────── Single Listen Pass ──────────────────────
    def _listen_once(self) -> Optional[str]:
        """
        Block until speech is detected and recognized.
        Returns the transcript string, or None on failure.
        """
        try:
            with sr.Microphone() as source:
                if not self._calibrated:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.5)

                log.info("Listening...", extra={"event": "listen_start"})
                audio = self._recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT,
                    phrase_time_limit=PHRASE_TIMEOUT,
                )

            log.info("Audio captured — transcribing...", extra={"event": "transcribe_start"})
            # Try Google first, fall back to Sphinx (offline)
            try:
                text = self._recognizer.recognize_google(audio, language="en-US")
                log.info(f"Google STT: '{text}'", extra={"event": "stt_google", "text": text})
                return text
            except sr.UnknownValueError:
                log.info("Google STT: could not understand audio")
                return None
            except sr.RequestError:
                log.warning("Google STT unavailable — trying Sphinx offline")
                try:
                    text = self._recognizer.recognize_sphinx(audio)
                    log.info(f"Sphinx STT: '{text}'", extra={"event": "stt_sphinx", "text": text})
                    return text
                except Exception:
                    return None

        except sr.WaitTimeoutError:
            return None  # silence — normal
        except Exception as e:
            log.error(f"Listen error: {e}", extra={"event": "listen_error"})
            return None

    # ─────────────────────── Main Listen Loop ────────────────────────
    async def listen_loop(self):
        """
        Async listen loop — runs calibration then continuously listens.
        Detected speech fires the on_transcript callback.
        """
        self._loop    = asyncio.get_running_loop()
        self._running = True

        # Calibrate in executor (non-blocking)
        await self._loop.run_in_executor(self._executor, self._calibrate)

        log.info("Audio listen loop started", extra={"event": "loop_start"})

        while self._running:
            try:
                transcript = await self._loop.run_in_executor(
                    self._executor, self._listen_once
                )
                if transcript and self._on_transcript:
                    # Fire callback into event loop
                    asyncio.create_task(self._on_transcript(transcript))

                await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error(f"Listen loop error: {e}", extra={"event": "loop_error"})
                await asyncio.sleep(1)

        log.info("Audio listen loop stopped", extra={"event": "loop_stop"})

    # ─────────────────────── TTS ─────────────────────────────────────
    async def speak_async(self, text: str):
        """Speak text without blocking the event loop."""
        if not text:
            return
        loop = asyncio.get_running_loop()
        log.info(f"Speaking: '{text[:60]}...'", extra={"event": "tts_speak"})
        await loop.run_in_executor(self._executor, self._tts.speak_blocking, text)

    # ─────────────────────── Shutdown ────────────────────────────────
    def shutdown(self):
        self._running = False
        self._executor.shutdown(wait=True, timeout=5.0)
        log.info("AudioEngine shutdown", extra={"event": "audio_shutdown"})