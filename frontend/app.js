/**
 * J.A.R.V.I.S — Unified Intelligence Core
 * Frontend Application — app.js
 *
 * Handles:
 *  - Arc Reactor canvas animation (idle / listening / processing / speaking)
 *  - Audio waveform visualizer
 *  - System diagnostics mock telemetry
 *  - State machine (IDLE → LISTENING → PROCESSING → SPEAKING → IDLE)
 *  - Chat history & terminal log
 *  - WebSocket connection to Python backend (ws://localhost:8765)
 *  - Fallback: OpenRouter LLM via backend API in demo mode
 *  - Web Speech API for voice input + TTS output
 */

'use strict';

/* ═══════════════════════════════ CONFIG ═══════════════════════════════ */
const CONFIG = {
  WS_URL:          window.location.hostname === 'localhost' ? 'ws://localhost:8765' : '',
  RECONNECT_MS:    3000,
  DEMO_MODE:       false,
  OPENROUTER_MODEL: 'anthropic/claude-sonnet-4',
};

/* ═══════════════════════════════ STATE MACHINE ═══════════════════════════════ */
const STATES = { IDLE:'IDLE', LISTENING:'LISTENING', PROCESSING:'PROCESSING', SPEAKING:'SPEAKING' };
let currentState = STATES.IDLE;

function setState(state) {
  currentState = state;
  document.body.className = state.toLowerCase();
  document.getElementById('statusText').textContent = state;
  document.getElementById('coreLabel').textContent = state;

  const hints = {
    IDLE:       'Awaiting command...',
    LISTENING:  'Listening to audio input...',
    PROCESSING: 'Analyzing with neural network...',
    SPEAKING:   'Generating audio response...',
  };
  document.getElementById('coreSublabel').textContent = hints[state];

  const voiceBtn = document.getElementById('voiceBtn');
  const voiceHint = document.getElementById('voiceHint');
  voiceBtn.className = 'voice-btn ' + (state === STATES.LISTENING ? 'listening' : state === STATES.PROCESSING ? 'processing' : '');
  voiceHint.textContent = state === STATES.IDLE ? 'CLICK TO SPEAK' : state === STATES.LISTENING ? 'LISTENING...' : state === STATES.PROCESSING ? 'PROCESSING...' : 'SPEAKING...';

  addTerminalLine(`[SYS ] State → ${state}`, state === STATES.IDLE ? '' : 'highlight');
}

/* ═══════════════════════════════ HUD CLOCK ═══════════════════════════════ */
function updateClock() {
  const now = new Date();
  document.getElementById('hudClock').textContent =
    now.toTimeString().slice(0,8);
  document.getElementById('hudDate').textContent =
    now.toDateString().toUpperCase();
}
updateClock();
setInterval(updateClock, 1000);

/* ═══════════════════════════════ UPTIME ═══════════════════════════════ */
const bootTime = Date.now();
setInterval(() => {
  const s = Math.floor((Date.now() - bootTime) / 1000);
  const h = String(Math.floor(s/3600)).padStart(2,'0');
  const m = String(Math.floor((s%3600)/60)).padStart(2,'0');
  const sec = String(s%60).padStart(2,'0');
  const el = document.getElementById('uptimeVal');
  if (el) el.textContent = `${h}:${m}:${sec}`;
}, 1000);

/* ═══════════════════════════════ MOCK DIAGNOSTICS ═══════════════════════════════ */
let queryCount = 0;
function updateDiagnostics() {
  if (!document.getElementById('cpuBar')) return;
  const t = Date.now() / 1000;
  const base = { cpu: 18, mem: 42, neural: 30, audio: 10 };
  const offsets = {
    cpu:    Math.sin(t * 0.7) * 12 + Math.random() * 6,
    mem:    Math.sin(t * 0.3) *  6 + Math.random() * 3,
    neural: currentState === STATES.PROCESSING ? 75 + Math.random() * 20
          : currentState === STATES.LISTENING   ? 50 + Math.random() * 15
          : Math.sin(t * 0.5) * 10 + Math.random() * 5,
    audio:  currentState === STATES.LISTENING  ? 60 + Math.random() * 30
          : currentState === STATES.SPEAKING    ? 70 + Math.random() * 25
          : Math.random() * 8,
  };
  ['cpu','mem','neural','audio'].forEach(k => {
    const val = Math.min(99, Math.max(3, base[k] + offsets[k]));
    document.getElementById(k + 'Bar').style.width = val + '%';
    document.getElementById(k + 'Val').textContent = Math.round(val) + '%';
  });
}
setInterval(updateDiagnostics, 500);

/* ═══════════════════════════════ TERMINAL LOG ═══════════════════════════════ */
const termLog = document.getElementById('terminalLog');
function addTerminalLine(text, cls = '') {
  const ts = new Date().toTimeString().slice(0,8);
  const el = document.createElement('div');
  el.className = 't-line' + (cls ? ' ' + cls : '');
  el.textContent = `[${ts}] ${text}`;
  termLog.appendChild(el);
  // Keep max 80 lines
  while (termLog.children.length > 80) termLog.removeChild(termLog.firstChild);
  termLog.scrollTop = termLog.scrollHeight;
}

/* ═══════════════════════════════ CHAT ═══════════════════════════════ */
const chatHistory = document.getElementById('chatHistory');
const conversationHistory = []; // multi-turn context for demo mode

function addMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = 'chat-msg ' + (role === 'jarvis' ? 'jarvis' : 'user');
  const timeStr = new Date().toTimeString().slice(0,8);
  msg.innerHTML = `
    <div class="msg-avatar">${role === 'jarvis' ? 'J' : 'U'}</div>
    <div class="msg-content">
      <span class="msg-sender">${role === 'jarvis' ? 'JARVIS' : 'YOU'}</span>
      <p>${escapeHtml(text)}</p>
      <span class="msg-time">${timeStr}</span>
    </div>`;
  chatHistory.appendChild(msg);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

document.getElementById('clearChatBtn').onclick = () => {
  chatHistory.innerHTML = '';
  conversationHistory.length = 0;
  addTerminalLine('[SYS ] Conversation log cleared');
};

/* ═══════════════════════════════ TOOL HIGHLIGHT ═══════════════════════════════ */
function fireToolHighlight(toolKey, durationMs = 2500) {
  const el = document.querySelector(`[data-tool="${toolKey}"]`);
  if (!el) return;
  el.classList.add('firing');
  const stat = el.querySelector('.tool-status');
  const prev = stat.textContent;
  stat.textContent = 'ACTIVE';
  addTerminalLine(`[TOOL] ${el.querySelector('.tool-name').textContent} invoked`, 'highlight');
  setTimeout(() => {
    el.classList.remove('firing');
    stat.textContent = prev;
  }, durationMs);
}

/* ═══════════════════════════════ LATENCY ═══════════════════════════════ */
let reqStart = 0;
function startLatency() { reqStart = performance.now(); }
function endLatency() {
  const ms = Math.round(performance.now() - reqStart);
  queryCount++;
  const latEl = document.getElementById('latencyVal');
  const qEl = document.getElementById('queriesVal');
  if (latEl) latEl.textContent = ms + 'ms';
  if (qEl) qEl.textContent = queryCount;
  return ms;
}

/* ═══════════════════════════════ ARC REACTOR CANVAS ═══════════════════════════════ */
const coreCanvas = document.getElementById('coreCanvas');
const ctx = coreCanvas.getContext('2d');
const CW = coreCanvas.width;
const CH = coreCanvas.height;
const CX = CW / 2, CY = CH / 2;

let arcAngle = 0;
let breathPhase = 0;
let particleRings = [];

// Particle class for processing state
class Particle {
  constructor() { this.reset(); }
  reset() {
    this.angle  = Math.random() * Math.PI * 2;
    this.radius = 80 + Math.random() * 60;
    this.speed  = (Math.random() * 0.02 + 0.01) * (Math.random() > .5 ? 1 : -1);
    this.size   = Math.random() * 2 + 0.5;
    this.alpha  = Math.random() * 0.8 + 0.2;
    this.decay  = Math.random() * 0.003 + 0.001;
  }
  update() {
    this.angle += this.speed;
    this.alpha -= this.decay;
    if (this.alpha <= 0) this.reset();
  }
  draw() {
    const x = CX + Math.cos(this.angle) * this.radius;
    const y = CY + Math.sin(this.angle) * this.radius;
    ctx.save();
    ctx.globalAlpha = Math.max(0, this.alpha);
    ctx.fillStyle = '#00dcff';
    ctx.shadowColor = '#00dcff';
    ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.arc(x, y, this.size, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }
}
const particles = Array.from({length: 60}, () => new Particle());

// Ripple wave class for listening state
class Ripple {
  constructor(r) { this.r = r; this.alpha = .7; }
  update() { this.r += 1.8; this.alpha -= 0.012; }
  dead() { return this.alpha <= 0; }
  draw() {
    ctx.save();
    ctx.globalAlpha = Math.max(0, this.alpha);
    ctx.strokeStyle = '#00dcff';
    ctx.shadowColor = '#00dcff'; ctx.shadowBlur = 8;
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.arc(CX, CY, this.r, 0, Math.PI * 2); ctx.stroke();
    ctx.restore();
  }
}
let ripples = [];
let rippleTimer = 0;

function spawnRipple() {
  ripples.push(new Ripple(45));
}

function drawCore(ts) {
  ctx.clearRect(0, 0, CW, CH);
  breathPhase += 0.025;
  arcAngle    += 0.008;

  const breath = Math.sin(breathPhase);

  // ── Outer ambient glow ──
  const glowR = 180 + breath * 8;
  const grad = ctx.createRadialGradient(CX, CY, 60, CX, CY, glowR);
  grad.addColorStop(0, 'rgba(0,220,255,0.10)');
  grad.addColorStop(1, 'transparent');
  ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(CX, CY, glowR, 0, Math.PI*2); ctx.fill();

  // ── Concentric rings (speaking: pulsing, else static) ──
  const ringCount = 5;
  for (let i = ringCount; i >= 1; i--) {
    const baseR = i * 34;
    let r = baseR;
    let alpha = 0.08 + i * 0.015;
    if (currentState === STATES.SPEAKING) {
      r = baseR + Math.sin(breathPhase * 3 + i * 0.9) * 12;
      alpha = 0.1 + Math.abs(Math.sin(breathPhase * 4 + i)) * 0.35;
    } else if (currentState === STATES.IDLE) {
      r = baseR + breath * 4;
      alpha = 0.06 + breath * 0.04;
    }
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = '#00dcff';
    ctx.lineWidth = currentState === STATES.SPEAKING ? 1.5 : 1;
    ctx.shadowColor = '#00dcff'; ctx.shadowBlur = 12;
    ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI*2); ctx.stroke();
    ctx.restore();
  }

  // ── Listening ripples ──
  if (currentState === STATES.LISTENING) {
    rippleTimer++;
    if (rippleTimer % 18 === 0) spawnRipple();
    ripples = ripples.filter(r => !r.dead());
    ripples.forEach(r => { r.update(); r.draw(); });
  }

  // ── Processing particles ──
  if (currentState === STATES.PROCESSING) {
    particles.forEach(p => { p.update(); p.draw(); });

    // Spinning outer arc segments
    for (let i = 0; i < 6; i++) {
      const a = arcAngle * 3 + (Math.PI * 2 / 6) * i;
      ctx.save();
      ctx.globalAlpha = 0.5;
      ctx.strokeStyle = '#00dcff';
      ctx.shadowColor = '#00dcff'; ctx.shadowBlur = 14;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(CX, CY, 155, a, a + 0.6);
      ctx.stroke();
      ctx.restore();
    }
  }

  // ── Rotating hexagonal data rings ──
  drawHexRing(CX, CY, 72, arcAngle, '#00dcff', 0.55);
  drawHexRing(CX, CY, 96, -arcAngle * 1.4, '#0066ff', 0.35);
  if (currentState !== STATES.IDLE) {
    drawHexRing(CX, CY, 120, arcAngle * 0.7, '#7b2dff', 0.25);
  }

  // ── Inner core disc ──
  const coreAlpha = currentState === STATES.PROCESSING ? 0.55 + Math.sin(breathPhase * 8) * 0.2
                  : currentState === STATES.LISTENING   ? 0.4  + Math.sin(breathPhase * 5) * 0.15
                  : currentState === STATES.SPEAKING    ? 0.45 + Math.sin(breathPhase * 6) * 0.2
                  : 0.2 + breath * 0.08;

  const innerGrad = ctx.createRadialGradient(CX, CY, 0, CX, CY, 44);
  innerGrad.addColorStop(0, `rgba(0,220,255,${coreAlpha})`);
  innerGrad.addColorStop(0.6, `rgba(0,102,255,${coreAlpha * 0.5})`);
  innerGrad.addColorStop(1, 'transparent');
  ctx.fillStyle = innerGrad; ctx.beginPath(); ctx.arc(CX, CY, 44, 0, Math.PI*2); ctx.fill();

  // ── Center dot ──
  ctx.save();
  ctx.globalAlpha = 0.9;
  ctx.shadowColor = '#00dcff'; ctx.shadowBlur = 30;
  ctx.fillStyle = '#00dcff';
  ctx.beginPath(); ctx.arc(CX, CY, 6, 0, Math.PI * 2); ctx.fill();
  ctx.restore();

  requestAnimationFrame(drawCore);
}

function drawHexRing(cx, cy, r, angle, color, alpha) {
  const sides = 6;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.shadowColor = color; ctx.shadowBlur = 8;
  ctx.lineWidth = 1;
  ctx.translate(cx, cy);
  ctx.rotate(angle);
  ctx.beginPath();
  for (let i = 0; i <= sides; i++) {
    const a = (Math.PI * 2 / sides) * i;
    i === 0 ? ctx.moveTo(Math.cos(a)*r, Math.sin(a)*r) : ctx.lineTo(Math.cos(a)*r, Math.sin(a)*r);
  }
  ctx.stroke();
  ctx.restore();
}

requestAnimationFrame(drawCore);

/* ═══════════════════════════════ AUDIO WAVEFORM CANVAS ═══════════════════════════════ */
const wvCanvas = document.getElementById('waveformCanvas');
const wvCtx    = wvCanvas ? wvCanvas.getContext('2d') : null;
let wvPhase    = 0;

function drawWaveform() {
  if (!wvCanvas || !wvCtx) return;
  const W = wvCanvas.width, H = wvCanvas.height;
  wvCtx.clearRect(0, 0, W, H);
  wvPhase += currentState === STATES.LISTENING ? 0.18 : currentState === STATES.SPEAKING ? 0.12 : 0.04;

  const amp = currentState === STATES.LISTENING  ? 22 + Math.random() * 10
            : currentState === STATES.SPEAKING    ? 16 + Math.sin(wvPhase * 2) * 8
            : currentState === STATES.PROCESSING  ? 8
            : 3;

  wvCtx.strokeStyle = '#00dcff';
  wvCtx.lineWidth   = 1.5;
  wvCtx.shadowColor = '#00dcff';
  wvCtx.shadowBlur  = 8;
  wvCtx.globalAlpha = 0.85;
  wvCtx.beginPath();

  const steps = 80;
  for (let i = 0; i <= steps; i++) {
    const x = (i / steps) * W;
    const noise = currentState === STATES.LISTENING ? (Math.random() - 0.5) * 8 : 0;
    const y = H/2 + Math.sin(wvPhase + i * 0.28) * amp
                  + Math.sin(wvPhase * 1.7 + i * 0.15) * (amp * 0.4)
                  + noise;
    i === 0 ? wvCtx.moveTo(x, y) : wvCtx.lineTo(x, y);
  }
  wvCtx.stroke();
  requestAnimationFrame(drawWaveform);
}
if (wvCanvas) requestAnimationFrame(drawWaveform);

/* ═══════════════════════════════ SPEECH API ═══════════════════════════════ */
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening  = false;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.continuous  = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onresult = (e) => {
    const transcript = Array.from(e.results)
      .map(r => r[0].transcript).join('');
    if (e.results[e.results.length - 1].isFinal) {
      addTerminalLine(`[MIC ] Captured: "${transcript.slice(0,40)}..."`, 'highlight');
      handleUserInput(transcript);
    }
  };
  recognition.onerror = (e) => {
    addTerminalLine(`[MIC ] Error: ${e.error}`, 'warn');
    setState(STATES.IDLE);
    isListening = false;
  };
  recognition.onend = () => { isListening = false; };
} else {
  addTerminalLine('[MIC ] Web Speech API not supported — use text input', 'warn');
}

function speak(text) {
  return new Promise(resolve => {
    if (!('speechSynthesis' in window)) { resolve(); return; }
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate   = 1.0;
    utter.pitch  = 0.9;
    // Prefer a male UK voice if available
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v => /google uk english male/i.test(v.name))
                   || voices.find(v => /en-gb/i.test(v.lang) && v.gender !== 'female')
                   || voices[0];
    if (preferred) utter.voice = preferred;
    utter.onstart = () => setState(STATES.SPEAKING);
    utter.onend   = () => { setState(STATES.IDLE); resolve(); };
    utter.onerror = () => { setState(STATES.IDLE); resolve(); };
    window.speechSynthesis.speak(utter);
  });
}

/* ═══════════════════════════════ WEBSOCKET (BACKEND) ═══════════════════════════════ */
let ws = null;
let wsConnected = false;

function checkServerlessAPI() {
  fetch('/api/health')
    .then(r => r.json())
    .then(data => addTerminalLine(`[API ] ${data.message}`, 'ok'))
    .catch(() => addTerminalLine('[API ] Backend warming up — retry on first query', 'warn'));
}

function connectWS() {
  if (!CONFIG.WS_URL) {
    addTerminalLine('[SYS ] Serverless mode — REST API auto-starts with the app', 'ok');
    checkServerlessAPI();
    return;
  }
  try {
    ws = new WebSocket(CONFIG.WS_URL);
    ws.onopen  = () => {
      wsConnected = true;
      CONFIG.DEMO_MODE = false;
      addTerminalLine('[WS  ] Backend connected', 'ok');
    };
    ws.onclose = () => {
      wsConnected = false;
      addTerminalLine('[WS  ] Backend disconnected — retrying...', 'warn');
      setTimeout(connectWS, CONFIG.RECONNECT_MS);
    };
    ws.onerror = () => {
      addTerminalLine('[WS  ] WebSocket error — retrying...', 'warn');
    };
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      handleBackendMessage(data);
    };
  } catch {
    addTerminalLine('[WS  ] Could not connect — retrying...', 'warn');
    setTimeout(connectWS, CONFIG.RECONNECT_MS);
  }
}
connectWS();

function handleBackendMessage(data) {
  const lat = endLatency();
  addTerminalLine(`[RESP] ${data.type || 'response'} received (${lat}ms)`, 'ok');

  if (data.tool) fireToolHighlight(data.tool);
  if (data.log)  addTerminalLine(`[TOOL] ${data.log}`);

  const reply = data.response || data.text || '';
  if (reply) {
    addMessage('jarvis', reply);
    speak(reply);
  } else {
    setState(STATES.IDLE);
  }
}

/* ═══════════════════════════════ LLM API (DEMO / FALLBACK) ═══════════════════════════════ */
const SYSTEM_PROMPT = `You are J.A.R.V.I.S — Just A Rather Very Intelligent System — the AI assistant created by Tony Stark. You are highly articulate, confident, and subtly witty. You:
- Answer concisely (1–3 sentences for simple queries, more for complex ones)
- Identify query intent: math/science → note you'd invoke WolframAlpha; weather → note you'd check OpenWeatherMap; scheduling → confirm and note the action
- Maintain context across the conversation
- For greetings, respond in character as JARVIS
- Never break character`;

async function askLLM(userText) {
  conversationHistory.push({ role: 'user', content: userText });

  const intent = classifyIntent(userText);
  if (intent !== 'llm') {
    fireToolHighlight(intent, 3000);
    addTerminalLine(`[ROUT] Intent → ${intent.toUpperCase()} tool`, 'highlight');
  } else {
    fireToolHighlight('llm', 2000);
  }

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: userText }),
    });
    const data = await response.json();
    const reply = data.response || 'I apologise — I encountered an issue processing that request.';
    conversationHistory.push({ role: 'assistant', content: reply });
    return reply;
  } catch (err) {
    addTerminalLine(`[ERR ] OpenRouter API: ${err.message}`, 'warn');
    return getFallbackResponse(userText);
  }
}

/* Simple intent classifier for tool routing */
function classifyIntent(text) {
  const t = text.toLowerCase();
  if (/weather|temperature|forecast|rain|sunny|humidity|wind/.test(t)) return 'weather';
  if (/calculate|integral|derivative|equation|prime|square root|math|solve|formula/.test(t)) return 'wolfram';
  if (/search|find|latest|news|who is|what is|google/.test(t)) return 'search';
  if (/schedule|remind|timer|alarm|calendar|appointment|set a/.test(t)) return 'scheduler';
  return 'llm';
}

/* Offline fallback */
function getFallbackResponse(text) {
  const t = text.toLowerCase();
  if (/hello|hi|hey/.test(t)) return "Hello. All systems are operational and I am at your service.";
  if (/time/.test(t))         return `The current time is ${new Date().toLocaleTimeString()}.`;
  if (/date/.test(t))         return `Today is ${new Date().toDateString()}.`;
  if (/weather/.test(t))      return "I'd normally query OpenWeatherMap for live forecasts, but my network link is currently unavailable.";
  if (/thank/.test(t))        return "Of course. It's what I'm here for.";
  if (/who are you|your name/.test(t)) return "I am J.A.R.V.I.S — Just A Rather Very Intelligent System.";
  return "I received your query but my primary LLM link is offline. Please check your API configuration.";
}

/* ═══════════════════════════════ MAIN INPUT HANDLER ═══════════════════════════════ */
async function handleUserInput(text) {
  if (!text.trim()) return;
  if (currentState !== STATES.IDLE && currentState !== STATES.LISTENING) return;

  addMessage('user', text);
  addTerminalLine(`[USER] "${text.slice(0,50)}${text.length > 50 ? '...' : ''}"`, 'highlight');
  setState(STATES.PROCESSING);
  startLatency();

  let reply;
  if (!CONFIG.DEMO_MODE && wsConnected && ws) {
    ws.send(JSON.stringify({ type: 'query', text }));
    // response handled in handleBackendMessage
    return;
  } else if (!CONFIG.DEMO_MODE && !CONFIG.WS_URL) {
    // Serverless mode
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      handleBackendMessage(data);
    } catch (err) {
      addTerminalLine(`[ERR ] API: ${err.message}`, 'warn');
      setState(STATES.IDLE);
    }
    return;
  }

  // Demo mode: use backend OpenRouter API
  reply = await askLLM(text);
  const lat = endLatency();
  addTerminalLine(`[LLM ] Response ready (${lat}ms)`, 'ok');
  addMessage('jarvis', reply);
  await speak(reply);
  setState(STATES.IDLE);
}

/* ═══════════════════════════════ UI BINDINGS ═══════════════════════════════ */
const voiceBtn  = document.getElementById('voiceBtn');
const textInput = document.getElementById('textInput');
const sendBtn   = document.getElementById('sendBtn');

voiceBtn.addEventListener('click', () => {
  if (currentState !== STATES.IDLE) {
    // Cancel if already active
    if (recognition && isListening) { recognition.stop(); }
    window.speechSynthesis.cancel();
    setState(STATES.IDLE);
    return;
  }
  if (!recognition) {
    addTerminalLine('[MIC ] SpeechRecognition not available', 'warn');
    return;
  }
  setState(STATES.LISTENING);
  isListening = true;
  try { recognition.start(); }
  catch { setState(STATES.IDLE); isListening = false; }
});

sendBtn.addEventListener('click', () => {
  const val = textInput.value.trim();
  textInput.value = '';
  if (val) handleUserInput(val);
});

textInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendBtn.click();
  }
});

// Click core canvas as voice trigger shortcut
coreCanvas.addEventListener('click', () => voiceBtn.click());

/* ═══════════════════════════════ BOOT SEQUENCE ═══════════════════════════════ */
const bootLines = [
  '[BOOT] Initializing J.A.R.V.I.S neural framework...',
  '[BOOT] Loading intent classification models...',
  '[BOOT] Calibrating audio pipeline...',
  '[BOOT] Connecting to tool APIs...',
  '[BOOT] WolframAlpha API → standby',
  '[BOOT] OpenWeatherMap API → standby',
  '[BOOT] DuckDuckGo Search  → standby',
  '[BOOT] Scheduler module   → armed',
  '[SYS ] Boot complete — all systems nominal',
];
bootLines.forEach((line, i) => {
  setTimeout(() => addTerminalLine(line, line.includes('nominal') ? 'ok' : ''), 400 + i * 220);
});
setTimeout(() => {
  addTerminalLine('[SYS ] Click the core or microphone button to speak', 'highlight');
  // Hide preloader with fade out
  const preloader = document.getElementById('preloader');
  preloader.classList.add('fade-out');
}, 400 + bootLines.length * 220);
