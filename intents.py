"""
J.A.R.V.I.S — intents.py
=========================
Intelligent intent classification and tool-routing pipeline.

Tools:
  - LLMTool        : OpenRouter LLM (primary brain, with memory)
  - WolframTool    : WolframAlpha for math / science / factual
  - WeatherTool    : OpenWeatherMap live forecasts
  - WebSearchTool  : DuckDuckGo search API
  - SchedulerTool  : Local time / timer / reminder management
  - FallbackTool   : Offline rule-based responses when all APIs fail
"""

import asyncio
import json
import os
import re
import subprocess
import time
import urllib.parse
from datetime import datetime
from typing import Any, Optional, Dict, Callable
from abc import ABC, abstractmethod

import aiohttp

from logger import get_logger
from config import get_config
from resilient import CircuitBreaker, retry_with_backoff, bulkhead

# Get configuration singleton
_config = get_config()

log = get_logger("intents")

# Resilience patterns for external services
# Circuit breakers for each external API service
llm_circuit_breaker = CircuitBreaker(
    failure_threshold=_config.external_services.failure_threshold,
    recovery_timeout=_config.external_services.recovery_timeout,
    name="llm"
)

wolfram_circuit_breaker = CircuitBreaker(
    failure_threshold=_config.external_services.failure_threshold,
    recovery_timeout=_config.external_services.recovery_timeout,
    name="wolfram"
)

weather_circuit_breaker = CircuitBreaker(
    failure_threshold=_config.external_services.failure_threshold,
    recovery_timeout=_config.external_services.recovery_timeout,
    name="weather"
)

search_circuit_breaker = CircuitBreaker(
    failure_threshold=_config.external_services.failure_threshold,
    recovery_timeout=_config.external_services.recovery_timeout,
    name="search"
)

# ─── API Keys (from configuration) ────────────────────────────────────
OPENROUTER_API_KEY = _config.api_keys.openrouter
OPENROUTER_MODEL   = _config.openrouter_model
WOLFRAM_APP_ID     = _config.api_keys.wolfram
OPENWEATHER_API_KEY= _config.api_keys.openweather
DEFAULT_CITY       = _config.default_city


# ═══════════════════════════════ BASE TOOL ══════════════════════════════════
class BaseTool:
    name = "base"

    async def run(self, text: str, context: list) -> dict:
        raise NotImplementedError

    def _result(self, response: str, tool: str = None, log_msg: str = "") -> dict:
        return {
            "response": response,
            "tool":     tool or self.name,
            "log":      log_msg or f"{self.name} responded",
        }


# ═══════════════════════════════ LLM TOOL ═══════════════════════════════════
# ═══════════════════════════════ LLM TOOL ═══════════════════════════════════
class LLMTool(BaseTool):
    """
    OpenRouter LLM tool — routes to Claude and other models via OpenRouter.
    Maintains a rolling conversational context window.
    """
    name = "llm"

    SYSTEM_PROMPT = (
        "You are J.A.R.V.I.S — Just A Rather Very Intelligent System, "
        "the AI assistant created by Tony Stark. You are articulate, confident, "
        "subtly witty, and extremely helpful. Keep responses concise (1–4 sentences) "
        "unless asked for detail. Never break character."
    )

    @llm_circuit_breaker.async_decorator
    @retry_with_backoff(
        max_attempts=_config.external_services.max_retries,
        base_delay=_config.external_services.base_delay,
        max_delay=_config.external_services.max_delay,
        name="llm_api"
    )
    @bulkhead(max_concurrent=5, name="llm")
    async def _call_llm_api(self, payload: dict, headers: dict, url: str) -> dict:
        """Call OpenRouter API with resilience patterns."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=_config.external_services.http_timeout)
            ) as r:
                return await r.json()

    async def run(self, text: str, context: list) -> dict:
        if not OPENROUTER_API_KEY:
            return FallbackTool().run_sync(text)

        messages = list(context)
        messages.append({"role": "user", "content": text})

        payload = {
            "model": OPENROUTER_MODEL,
            "max_tokens": 800,
            "messages": [{"role": "system", "content": self.SYSTEM_PROMPT}] + messages,
        }
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Sahhhiiillllll/JARVIS---AI-Intelligence-System-LLM",
            "X-Title": "J.A.R.V.I.S",
        }
        url = "https://openrouter.ai/api/v1/chat/completions"

        try:
            data = await self._call_llm_api(payload, headers, url)
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not reply:
                raise ValueError("Empty LLM response")
            log.info("LLM response received", extra={"chars": len(reply)})
            return self._result(reply, "llm", "OpenRouter LLM responded")

        except Exception as e:
            log.error(f"LLM error: {e}", extra={"event": "llm_error"})
            return FallbackTool().run_sync(text)
class WolframTool(BaseTool):
    """WolframAlpha Short Answer API for mathematical and scientific queries."""
    name = "wolfram"

    @wolfram_circuit_breaker.async_decorator
    @retry_with_backoff(
        max_attempts=_config.external_services.max_retries,
        base_delay=_config.external_services.base_delay,
        max_delay=_config.external_services.max_delay,
        name="wolfram_api"
    )
    @bulkhead(max_concurrent=3, name="wolfram")
    async def _call_wolfram_api_v1(self, params: dict) -> tuple[int, str]:
        """Call WolframAlpha v1 API with resilience patterns."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.wolframalpha.com/v1/result",
                params=params, timeout=aiohttp.ClientTimeout(total=_config.external_services.wolfram_timeout)
            ) as r:
                return r.status, await r.text()

    @wolfram_circuit_breaker.async_decorator
    @retry_with_backoff(
        max_attempts=_config.external_services.max_retries,
        base_delay=_config.external_services.base_delay,
        max_delay=_config.external_services.max_delay,
        name="wolfram_full_query"
    )
    @bulkhead(max_concurrent=3, name="wolfram_full")
    async def _call_wolfram_api_v2(self, params: dict) -> dict:
        """Call WolframAlpha v2 API with resilience patterns."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.wolframalpha.com/v2/query",
                params=params, timeout=aiohttp.ClientTimeout(total=_config.external_services.wolfram_timeout + 2)
            ) as r:
                return await r.json(content_type=None)

    async def run(self, text: str, context: list) -> dict:
        if not WOLFRAM_APP_ID:
            log.warning("WolframAlpha APP_ID not set — falling back to LLM")
            return await LLMTool().run(text, context)

        query = re.sub(r'\b(calculate|compute|what is|solve|evaluate)\b', '', text, flags=re.I).strip()
        params = {"i": query, "appid": WOLFRAM_APP_ID, "output": "plaintext"}

        try:
            status, answer = await self._call_wolfram_api_v1(params)
            if status == 200:
                reply = f"According to WolframAlpha: {answer}"
                log.info(f"Wolfram answered: {reply[:60]}", extra={"event": "wolfram_ok"})
                return self._result(reply, "wolfram", f"WolframAlpha → {reply[:60]}")
            else:
                # Fallback to full query API
                reply = await self._full_query(query)
                return self._result(reply, "wolfram", f"WolframAlpha (full query) → {reply[:60]}")

        except Exception as e:
            log.error(f"Wolfram error: {e}", extra={"event": "wolfram_error"})
            return await LLMTool().run(text, context)

    async def _full_query(self, query: str) -> str:
        """Fallback to WolframAlpha full API and extract primary pod."""
        params = {"input": query, "appid": WOLFRAM_APP_ID, "format": "plaintext", "output": "JSON"}
        try:
            data = await self._call_wolfram_api_v2(params)

            pods = data.get("queryresult", {}).get("pods", [])
            for pod in pods:
                if pod.get("primary") or pod.get("id") == "Result":
                    for sub in pod.get("subpods", []):
                        text = sub.get("plaintext", "").strip()
                        if text:
                            return f"The result is {text}."
            return "WolframAlpha could not determine a result for that query."
        except Exception as e:
            log.error(f"Wolfram full query error: {e}", extra={"event": "wolfram_full_error"})
            return "WolframAlpha could not determine a result for that query."


# ═══════════════════════════════ WEATHER TOOL ════════════════════════════════
class WeatherTool(BaseTool):
    """OpenWeatherMap live weather data."""
    name = "weather"

    _COND_ICON = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
        "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
        "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌫️",
    }

    @weather_circuit_breaker.async_decorator
    @retry_with_backoff(
        max_attempts=_config.external_services.max_retries,
        base_delay=_config.external_services.base_delay,
        max_delay=_config.external_services.max_delay,
        name="weather_api"
    )
    @bulkhead(max_concurrent=5, name="weather")
    async def _call_weather_api(self, params: dict) -> dict:
        """Call Weather API with resilience patterns."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params=params, timeout=aiohttp.ClientTimeout(total=_config.external_services.weather_timeout)
            ) as r:
                if r.status != 200:
                    raise ValueError(f"HTTP {r.status}")
                return await r.json()

    async def run(self, text: str, context: list) -> dict:
        # Extract city from query, or use default
        city = self._extract_city(text) or DEFAULT_CITY

        if not OPENWEATHER_API_KEY:
            reply = (f"I'd retrieve the forecast for {city} via OpenWeatherMap, "
                     "but the API key is not configured.")
            return self._result(reply, "weather", "WeatherTool: API key missing")

        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        try:
            data = await self._call_weather_api(params)

            main  = data["main"]
            wind  = data.get("wind", {})
            cond  = data["weather"][0]["main"]
            desc  = data["weather"][0]["description"].capitalize()
            icon  = self._COND_ICON.get(cond, "🌡️")
            temp  = round(main["temp"])
            feels = round(main["feels_like"])
            hum   = main["humidity"]
            wind_s= round(wind.get("speed", 0) * 3.6)  # m/s → km/h

            reply = (
                f"{icon} In {city}: {desc}. "
                f"Temperature {temp}°C (feels like {feels}°C). "
                f"Humidity {hum}%, wind {wind_s} km/h."
            )
            log.info(f"Weather fetched for {city}", extra={"event": "weather_ok"})
            return self._result(reply, "weather", f"Weather API → {city}: {temp}°C, {desc}")

        except Exception as e:
            log.error(f"Weather error: {e}", extra={"event": "weather_error"})
            return await LLMTool().run(text, context)

    @staticmethod
    def _extract_city(text: str) -> Optional[str]:
        """Crude city extractor — looks for 'in <City>' or 'for <City>'."""
        m = re.search(r'\b(?:in|for|at)\s+([A-Z][a-zA-Z\s]{2,25}?)(?:\?|$|,)', text)
        return m.group(1).strip() if m else None


# ═══════════════════════════════ WEB SEARCH TOOL ═══════════════════════════════
class WebSearchTool(BaseTool):
    """DuckDuckGo Instant Answer API (no key required)."""
    name = "search"

    @search_circuit_breaker.async_decorator
    @retry_with_backoff(
        max_attempts=_config.external_services.max_retries,
        base_delay=_config.external_services.base_delay,
        max_delay=_config.external_services.max_delay,
        name="search_api"
    )
    @bulkhead(max_concurrent=5, name="search")
    async def _call_search_api(self, params: dict, headers: dict) -> dict:
        """Call Search API with resilience patterns."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.duckduckgo.com/",
                params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=_config.external_services.search_timeout),
            ) as r:
                return await r.json(content_type=None)

    async def run(self, text: str, context: list) -> dict:
        query = re.sub(r'\b(search|find|google|look up|what is|who is)\b', '',
                       text, flags=re.I).strip()
        try:
            data = await self._call_search_api(
                {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                {"User-Agent": "JARVIS/4.1"}
            )

            abstract = data.get("AbstractText", "").strip()
            answer   = data.get("Answer",       "").strip()
            topic    = data.get("RelatedTopics", [{}])[0].get("Text", "").strip() if data.get("RelatedTopics") else ""

            best = abstract or answer or topic
            if best:
                reply = f"Here's what I found: {best[:350]}"
                if data.get("AbstractURL"):
                    reply += f" (Source: {data['AbstractURL']})"
            else:
                # Fallback to LLM for queries DuckDuckGo can't answer
                log.info("DuckDuckGo returned no results — delegating to LLM")
                return await LLMTool().run(text, context)

            log.info(f"Web search complete for: {query[:40]}", extra={"event": "search_ok"})
            return self._result(reply, "search", f"DuckDuckGo → {query[:40]}")

        except Exception as e:
            log.error(f"Search error: {e}", extra={"event": "search_error"})
            return await LLMTool().run(text, context)


# ═══════════════════════════════ SCHEDULER TOOL ═══════════════════════════════
class SchedulerTool(BaseTool):
    """Local scheduling, time checks, and in-memory reminders."""
    name = "scheduler"

    _reminders: list = []  # simple in-memory store

    async def run(self, text: str, context: list) -> dict:
        t = text.lower()

        # ── Time / Date ──
        if re.search(r'\b(time|clock)\b', t):
            now = datetime.now().strftime("%I:%M %p")
            return self._result(f"The current time is {now}.", "scheduler", "Time query answered")

        if re.search(r'\b(date|today)\b', t):
            today = datetime.now().strftime("%A, %B %d, %Y")
            return self._result(f"Today is {today}.", "scheduler", "Date query answered")

        # ── Set reminder ──
        reminder_match = re.search(
            r'remind(?:er)?\s+(?:me\s+)?(?:to\s+)?(.+?)\s+(?:at|in)\s+([\d:apmAPM\s]+)',
            text,
            re.IGNORECASE,
        )
        if reminder_match:
            task = reminder_match.group(1).strip()
            when = reminder_match.group(2).strip()
            self._reminders.append({"task": task, "when": when, "set_at": datetime.now().isoformat()})
            reply = f"Understood. I've set a reminder to '{task}' at {when}."
            return self._result(reply, "scheduler", f"Reminder set: {task} @ {when}")

        # ── List reminders ──
        if re.search(r'\b(list|show)\s+(?:my\s+)?reminders?\b', t) or re.search(r'what are my reminders?', t):
            if not self._reminders:
                return self._result("You have no active reminders.", "scheduler", "No reminders")
            items = "; ".join(f"'{r['task']}' at {r['when']}" for r in self._reminders)
            return self._result(f"Active reminders: {items}.", "scheduler", f"{len(self._reminders)} reminders")

        # ── Generic fallback ──
        return self._result(
            "I can check the time, today's date, set reminders, and manage your schedule. What would you like?",
            "scheduler", "Scheduler general response"
        )


# ═══════════════════════════════ SYSTEM CONTROL TOOL ═══════════════════════════════
class SystemControlTool(BaseTool):
    """Executes native macOS commands (open, quit, volume, sleep)."""
    name = "system"

    def _format_url(self, target: str) -> str:
        target = target.strip()
        if target.startswith("http://") or target.startswith("https://"):
            return target
        if " " in target:
            import urllib.parse
            return f"https://www.google.com/search?q={urllib.parse.quote(target)}"
        if "." in target:
            return f"https://{target}"
        return f"https://www.{target}.com"

    async def run(self, text: str, context: list) -> dict:
        t = text.lower()

        # ── Open / Launch ──
        open_match = re.search(r'\b(open|launch|start|go to)\s+(?:the\s+)?(.+?)(?:\s+in\s+my\s+macbook|\s+app(?:lication)?)?(?:\s+and\s+.*)?$', t)
        if open_match:
            target_raw = open_match.group(2).strip()
            
            # Special case for "open X in Y browser"
            in_match = re.search(r'(.+)\s+in\s+([a-z0-9\s]+?)(?:\s+browser)?$', target_raw)
            if in_match:
                target = in_match.group(1).strip()
                browser = in_match.group(2).strip()
                target_url = self._format_url(target)
                try:
                    subprocess.run(["open", "-a", browser, target_url], check=True, stderr=subprocess.PIPE)
                    return self._result(f"I have opened {target} in {browser}.", "system", f"Opened {target} in {browser}")
                except subprocess.CalledProcessError:
                    pass

            # Detect if it's explicitly a website
            if any(ext in target_raw for ext in [".com", ".org", ".net", ".edu", ".gov", "website", "site", "webpage"]):
                clean_target = target_raw.replace("website", "").replace("site", "").replace("webpage", "").strip()
                if clean_target.startswith("the "):
                    clean_target = clean_target[4:]
                if clean_target:
                    target_url = self._format_url(clean_target)
                    try:
                        subprocess.run(["open", target_url], check=True, stderr=subprocess.PIPE)
                        return self._result(f"I have opened the website {clean_target}.", "system", f"Opened {clean_target}")
                    except Exception:
                        pass

            # Normal app open
            try:
                subprocess.run(["open", "-a", target_raw], check=True, stderr=subprocess.PIPE)
                return self._result(f"I have launched {target_raw}.", "system", f"Launched {target_raw}")
            except subprocess.CalledProcessError:
                # Fallback to basic open
                try:
                    subprocess.run(["open", target_raw], check=True, stderr=subprocess.PIPE)
                    return self._result(f"I have opened {target_raw}.", "system", f"Opened {target_raw}")
                except Exception:
                    return self._result(f"I was unable to find or launch '{target_raw}'.", "system", f"Failed to launch {target_raw}")

        # ── Close / Quit ──
        close_match = re.search(r'\b(close|quit|kill)\s+(.+?)(?:\s+app(?:lication)?)?$', t)
        if close_match:
            app_name = close_match.group(2).strip()
            try:
                subprocess.run(["osascript", "-e", f'quit app "{app_name}"'], check=True, stderr=subprocess.PIPE)
                return self._result(f"I have closed {app_name}.", "system", f"Closed {app_name}")
            except Exception:
                return self._result(f"I was unable to close '{app_name}'.", "system", f"Failed to close {app_name}")

        # ── Volume ──
        vol_match = re.search(r'\b(?:set\s+)?volume(?:\s+to)?\s+(\d+|max(?:imum)?|min(?:imum)?|mute|unmute)\b', t)
        if not vol_match:
            vol_match = re.search(r'\b(mute|unmute)\b', t)

        if vol_match:
            val = vol_match.group(1).strip()
            if val in ["mute", "unmute"]:
                state = "true" if val == "mute" else "false"
                subprocess.run(["osascript", "-e", f'set volume output muted {state}'])
                return self._result(f"System volume is now {val}d.", "system", f"Volume {val}d")
            elif val.isdigit():
                v = max(0, min(100, int(val)))
                subprocess.run(["osascript", "-e", f'set volume output volume {v}'])
                return self._result(f"System volume set to {v} percent.", "system", f"Volume set to {v}")
            elif "max" in val:
                subprocess.run(["osascript", "-e", 'set volume output volume 100'])
                return self._result("System volume set to maximum.", "system", "Volume max")
            elif "min" in val:
                subprocess.run(["osascript", "-e", 'set volume output volume 0'])
                return self._result("System volume set to minimum.", "system", "Volume min")

        # ── Sleep / Lock ──
        if ("sleep" in t or "lock" in t) and ("mac" in t or "system" in t or "screen" in t):
            subprocess.run(["pmset", "displaysleepnow"])
            return self._result("Putting the display to sleep.", "system", "System sleep/lock")

        # ── Battery ──
        if "battery" in t or "power" in t:
            try:
                out = subprocess.check_output(["pmset", "-g", "batt"], text=True)
                match = re.search(r'(\d+)%', out)
                if match:
                    pct = match.group(1)
                    status = "charging" if "charging" in out or "AC Power" in out else "discharging"
                    return self._result(f"The battery is at {pct} percent and is currently {status}.", "system", f"Battery {pct}%")
            except Exception:
                pass
            return self._result("I am unable to retrieve the battery status.", "system", "Battery check failed")

        # ── Dark / Light Mode ──
        if "dark mode" in t or "light mode" in t or "theme" in t:
            if "light" in t or "off" in t:
                script = 'tell application "System Events" to tell appearance preferences to set dark mode to false'
                mode = "light"
            else:
                script = 'tell application "System Events" to tell appearance preferences to set dark mode to true'
                mode = "dark"
            subprocess.run(["osascript", "-e", script])
            return self._result(f"I have switched the system to {mode} mode.", "system", f"Theme set to {mode}")

        # ── Screenshot ──
        if "screenshot" in t or "capture" in t:
            try:
                desktop = os.path.expanduser("~/Desktop")
                filename = f"{desktop}/Screenshot_{int(time.time())}.png"
                subprocess.run(["screencapture", filename], check=True)
                return self._result("I have taken a screenshot and saved it to your desktop.", "system", "Screenshot taken")
            except Exception:
                return self._result("I failed to take a screenshot.", "system", "Screenshot failed")

        # ── Empty Trash ──
        if "trash" in t and ("empty" in t or "clear" in t):
            subprocess.run(["osascript", "-e", 'tell application "Finder" to empty trash'])
            return self._result("The trash has been emptied.", "system", "Trash emptied")

        # ── Media Controls ──
        media_match = re.search(r'\b(play|pause|next|previous|skip)\b', t)
        if media_match and ("music" in t or "song" in t or "media" in t or "spotify" in t):
            action = media_match.group(1)
            
            if action == "play":
                song_match = re.search(r'play\s+(?:the\s+)?(?:song\s+|track\s+|music\s+)?(?:named\s+|called\s+)?(.+?)(?:\s+in\s+spotify|\s+on\s+spotify|\s+in\s+apple\s+music|\s+on\s+apple\s+music|\s+in\s+music|\s+on\s+music|\s+please)?$', t)
                if song_match:
                    song_name = song_match.group(1).strip()
                    ignored_words = {"", "some", "my", "the", "music", "song", "media", "spotify", "apple music", "some music", "a song", "any song", "something"}
                    if song_name not in ignored_words:
                        query = urllib.parse.quote(song_name)
                        if "music" in t and "spotify" not in t:
                            # Apple Music
                            script = f'tell application "Music" to play track "{song_name}"'
                            subprocess.run(["osascript", "-e", script], stderr=subprocess.DEVNULL)
                        else:
                            # Spotify
                            script = f'tell application "Spotify" to play track "spotify:search:{query}"'
                            subprocess.run(["osascript", "-e", script], stderr=subprocess.DEVNULL)
                        
                        return self._result(f"Playing '{song_name}' for you.", "system", f"Playing {song_name}")

            # Generic media controls fallback
            for app in ["Spotify", "Music"]:
                if action in ["play", "pause"]:
                    script = f'tell application "{app}" to playpause'
                elif action in ["next", "skip"]:
                    script = f'tell application "{app}" to next track'
                elif action == "previous":
                    script = f'tell application "{app}" to previous track'
                subprocess.run(["osascript", "-e", script], stderr=subprocess.DEVNULL)
            return self._result(f"I have executed the {action} command for your media.", "system", f"Media {action}")

        # ── Wi-Fi Toggle ──
        if "wifi" in t or "wi-fi" in t or "network" in t:
            if "on" in t or "enable" in t:
                subprocess.run(["networksetup", "-setairportpower", "en0", "on"])
                return self._result("Wi-Fi has been enabled.", "system", "WiFi on")
            elif "off" in t or "disable" in t:
                subprocess.run(["networksetup", "-setairportpower", "en0", "off"])
                return self._result("Wi-Fi has been disabled.", "system", "WiFi off")

        return self._result("I received a system command but I'm not sure how to execute it.", "system", "Unknown system command")


# ═══════════════════════════════ FALLBACK TOOL ═══════════════════════════════
class FallbackTool(BaseTool):
    """Offline rule-based responses when all APIs are unavailable."""
    name = "llm"

    _RESPONSES = {
        r'\b(hello|hi|hey|good\s*(morning|afternoon|evening))\b':
            "Hello. All systems are operational and I am at your service.",
        r'\b(thank|thanks|appreciate)\b':
            "Of course. It's what I'm here for.",
        r'\b(joke|funny|humor)\b':
            "I'm afraid my humor subroutines are in maintenance mode. Ask me something more practical.",
        r'\b(who (are|is) you|your name)\b':
            "I am J.A.R.V.I.S — Just A Rather Very Intelligent System.",
        r'\b(how are you|status)\b':
            "All primary subsystems are functioning within normal parameters.",
        r'\b(shutdown|exit|quit|goodbye|bye)\b':
            "Initiating standby protocol. It's been a pleasure.",
    }

    def run_sync(self, text: str) -> dict:
        t = text.lower()
        for pattern, response in self._RESPONSES.items():
            if re.search(pattern, t):
                return self._result(response, "llm", "Fallback rule matched")
        return self._result(
            "My primary intelligence network is temporarily offline. "
            "Please check the API configuration and try again.",
            "llm", "Fallback: offline"
        )

    async def run(self, text: str, context: list) -> dict:
        return self.run_sync(text)


# ═══════════════════════════════ INTENT ROUTER ═══════════════════════════════
class IntentRouter:
    """
    Classify user intent and dispatch to the appropriate tool.
    Maintains a rolling conversation context for multi-turn memory.
    """

    MAX_HISTORY = 20  # max turns to keep in context

    # (regex pattern, tool_key)
    INTENT_RULES: list[tuple[str, str]] = [
        # Scheduling / time
        (r'\b(time|clock|date|today|schedule|remind|reminder|alarm|timer|calendar|appointment)\b', 'scheduler'),
        # Weather
        (r'\b(weather|temperature|forecast|rain|sunny|cloud|humidity|wind speed|precipitation)\b', 'weather'),
        # Math / science
        (r'\b(calculate|compute|integral|derivative|equation|prime|square root|convert|formula|'
         r'how many|how much|what is \d|solve)\b', 'wolfram'),
        # Web search
        (r'\b(search|find|google|look up|latest|news|who is|define|meaning of|wikipedia)\b', 'search'),
        # System control
        (r'\b(open|launch|start|close|quit|volume|mute|unmute|sleep|battery|power|dark mode|light mode|theme|lock|screenshot|capture|trash|wifi|network|play|pause|next|previous|skip)\b', 'system'),
    ]

    def __init__(self):
        try:
            self._tools: dict[str, BaseTool] = {
                "llm":       LLMTool(),
                "wolfram":   WolframTool(),
                "weather":   WeatherTool(),
                "search":    WebSearchTool(),
                "scheduler": SchedulerTool(),
                "system":    SystemControlTool(),
                "fallback":  FallbackTool(),
            }
            self._context: list[dict] = []
            log.info("IntentRouter initialized", extra={"event": "router_init"})
        except Exception as e:
            log.error(f"Failed to initialize IntentRouter: {e}", extra={"event": "router_init_error"})
            raise

    def classify(self, text: str) -> str:
        """Return the tool key for the given input text."""
        lower = text.lower()
        for pattern, tool_key in self.INTENT_RULES:
            if re.search(pattern, lower):
                log.info(f"Intent classified → {tool_key}", extra={"pattern": pattern[:40]})
                return tool_key
        return "llm"

    async def route(self, text: str) -> dict:
        """Classify and execute the appropriate tool, then update context."""
        tool_key = self.classify(text)
        tool     = self._tools.get(tool_key, self._tools["llm"])

        log.info(f"Routing to tool: {tool_key}", extra={"event": "route", "tool": tool_key})

        # Pass current context (for LLM multi-turn)
        result = await tool.run(text, list(self._context))

        # Update rolling context
        self._context.append({"role": "user",      "content": text})
        self._context.append({"role": "assistant",  "content": result.get("response", "")})
        if len(self._context) > self.MAX_HISTORY * 2:
            self._context = self._context[-(self.MAX_HISTORY * 2):]

        return result