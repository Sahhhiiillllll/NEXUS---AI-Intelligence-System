# Auto-generated assets file to bypass Vercel filesystem stripping

INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>J.A.R.V.I.S — Unified Intelligence Core</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="space.css">
</head>
<body>
  <!-- Preloader Space Opening -->
  <div id="preloader" class="preloader">
    <div class="starfield"></div>
    <div class="nebula"></div>
    <div class="loading-text">INITIALIZING J.A.R.V.I.S...</div>
  </div>

  <!-- ═══════════════════════════════════ SCAN LINES OVERLAY ═══════════════════════════════════ -->
  <div class="scanlines"></div>
  <div class="noise-overlay"></div>

  <!-- ═══════════════════════════════════ HEADER BAR ═══════════════════════════════════ -->
  <header class="hud-header">
    <div class="header-left">
      <span class="logo-text">J.A.R.V.I.S V6.5</span>
      <span class="logo-sub">UNIVERSAL CHARACTER AI & CHAT ACCELERATOR</span>
    </div>
    <div class="header-center">
      <div class="status-pill" id="statusPill">
        <span class="status-dot"></span>
        <span id="statusText">STANDBY</span>
      </div>
    </div>
    <div class="header-right">
      <div class="hud-clock" id="hudClock">--:--:--</div>
      <div class="hud-date" id="hudDate">---</div>
    </div>
  </header>

  <!-- ═══════════════════════════════════ MAIN LAYOUT ═══════════════════════════════════ -->
  <main class="main-layout">

    <!-- ─────────────────── LEFT PANEL ─────────────────── -->
    <aside class="side-panel left-panel">

      <!-- Boot Sequence HUD -->
      <div class="panel-card boot-card" style="font-family: var(--font-display); background: rgba(0, 100, 200, 0.1); border: 1px solid rgba(0, 200, 255, 0.4); padding: 20px; text-transform: uppercase;">
        <div style="font-size: 24px; color: var(--c-cyan); font-weight: 900; letter-spacing: 4px; margin-bottom: 5px;">J.A.R.V.I.S V6.5</div>
        <div style="font-size: 10px; color: var(--c-text-dim); letter-spacing: 2px; margin-bottom: 20px;">UNIVERSAL CHARACTER AI & CHAT ACCELERATOR</div>
        
        <div class="boot-sequence" style="font-family: var(--font-mono); font-size: 11px; color: var(--c-cyan); line-height: 1.8; letter-spacing: 1px;">
          <div>LOADING HIGH-FREQUENCY NLP TOKENIZER... <span style="color: var(--c-ok); float: right;">READY</span></div>
          <div>INITIALIZING NEURAL CONTEXT STREAM... <span style="color: var(--c-ok); float: right;">ACTIVE</span></div>
          <div>PULLING LOCAL MEMORY VECTOR DATABASE... <span style="color: var(--c-ok); float: right;">COMPILED</span></div>
          <div>MONITORING HARDWARE TEMPERATURE SENSORS... <span style="color: var(--c-ok); float: right;">NORMAL</span></div>
          <div>ROUTING AUDIO PRE-PROCESSING FILTERS... <span style="color: var(--c-ok); float: right;">ACTIVE</span></div>
          <div>PARSING CUSTOM USER BEHAVIOR PATTERNS... <span style="color: var(--c-ok); float: right;">LOADED</span></div>
          <div>CALIBRATING SYNTHETIC MAPPING SENSORS... <span style="color: var(--c-ok); float: right;">SYNCHRONIZED</span></div>
          <div>CONNECTING CLOUD REPLICATOR MEMORY STACK... <span style="color: var(--c-ok); float: right;">SECURED</span></div>
        </div>
      </div>
    </aside>

    <!-- ─────────────────── CENTER: CORE ─────────────────── -->
    <section class="center-core">
      <!-- Arc Reactor Canvas -->
      <div class="core-wrapper">
        <canvas id="coreCanvas" width="420" height="420"></canvas>
        <div class="core-label" id="coreLabel">IDLE</div>
        <div class="core-sublabel" id="coreSublabel">Awaiting command...</div>
      </div>

      <!-- Voice Button -->
      <div class="voice-controls">
        <button class="voice-btn" id="voiceBtn" title="Hold to speak">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/>
          </svg>
        </button>
        <span class="voice-hint" id="voiceHint">CLICK TO SPEAK</span>
      </div>

      <!-- Text Input Fallback -->
      <div class="text-input-row">
        <input type="text" id="textInput" class="nexus-input" placeholder="Or type your command here..." autocomplete="off"/>
        <button class="send-btn" id="sendBtn">SEND</button>
      </div>
    </section>

    <!-- ─────────────────── RIGHT PANEL ─────────────────── -->
    <aside class="side-panel right-panel">

      <!-- Chat History -->
      <div class="panel-card chat-card">
        <div class="card-header">
          <span class="card-icon">◉</span>
          <span>CONVERSATION LOG</span>
          <button class="clear-btn" id="clearChatBtn" title="Clear history">✕</button>
        </div>
        <div class="chat-history" id="chatHistory">
          <div class="chat-msg nexus">
            <div class="msg-avatar">J</div>
            <div class="msg-content">
              <span class="msg-sender">NEXUS</span>
              <p>All systems initialized. Neural networks calibrated. How can I assist you today?</p>
              <span class="msg-time">BOOT</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Terminal Log -->
      <div class="panel-card terminal-card">
        <div class="card-header">
          <span class="card-icon">▶</span>
          <span>NEURAL TERMINAL</span>
          <span class="terminal-blink">●</span>
        </div>
        <div class="terminal-log" id="terminalLog">
          <div class="t-line">[BOOT] J.A.R.V.I.S core initialized</div>
          <div class="t-line">[BOOT] Loading neural weight matrices...</div>
          <div class="t-line">[BOOT] Audio pipeline calibrated</div>
          <div class="t-line">[BOOT] Intent classifier ready</div>
          <div class="t-line">[SYS ] All subsystems nominal ✓</div>
        </div>
      </div>

    </aside>
  </main>

  <!-- ═══════════════════════════════════ CORNER DECORATIONS ═══════════════════════════════════ -->
  <div class="corner corner-tl"></div>
  <div class="corner corner-tr"></div>
  <div class="corner corner-bl"></div>
  <div class="corner corner-br"></div>

  <script src="app.js"></script>
</body>
</html>
'''

STYLE_CSS = '''/* ═══════════════════════════════════════════════════════════════════
   J.A.R.V.I.S — UNIFIED INTELLIGENCE CORE
   Cyberpunk / Deep Space HUD Stylesheet
   ═══════════════════════════════════════════════════════════════════ */

/* ── Tokens ── */
:root {
  --c-bg:          #020608;
  --c-bg2:         #060d12;
  --c-panel:       rgba(0, 220, 255, 0.04);
  --c-border:      rgba(0, 220, 255, 0.15);
  --c-border-hi:   rgba(0, 220, 255, 0.45);
  --c-cyan:        #00dcff;
  --c-cyan-dim:    rgba(0, 220, 255, 0.6);
  --c-blue:        #0066ff;
  --c-purple:      #7b2dff;
  --c-warn:        #ffaa00;
  --c-ok:          #00ff88;
  --c-text:        #cce8f0;
  --c-text-dim:    #4a7a8a;
  --c-text-mid:    #7ab8cc;
  --font-display:  'Orbitron', monospace;
  --font-mono:     'Share Tech Mono', monospace;
  --font-body:     'Inter', sans-serif;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; }

body {
  background: var(--c-bg);
  color: var(--c-text);
  font-family: var(--font-body);
  font-size: 13px;
  position: relative;
}

/* ── Scan Lines ── */
.scanlines {
  pointer-events: none;
  position: fixed; inset: 0; z-index: 100;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.08) 2px,
    rgba(0,0,0,0.08) 4px
  );
}
.noise-overlay {
  pointer-events: none;
  position: fixed; inset: 0; z-index: 99;
  opacity: 0.02;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

/* ── Corner Decorations ── */
.corner {
  position: fixed; width: 28px; height: 28px; z-index: 200;
  pointer-events: none;
}
.corner-tl { top:10px; left:10px;  border-top:1px solid var(--c-cyan-dim); border-left:1px solid var(--c-cyan-dim); }
.corner-tr { top:10px; right:10px; border-top:1px solid var(--c-cyan-dim); border-right:1px solid var(--c-cyan-dim); }
.corner-bl { bottom:10px; left:10px;  border-bottom:1px solid var(--c-cyan-dim); border-left:1px solid var(--c-cyan-dim); }
.corner-br { bottom:10px; right:10px; border-bottom:1px solid var(--c-cyan-dim); border-right:1px solid var(--c-cyan-dim); }

/* ══════════ HEADER ══════════ */
.hud-header {
  position: fixed; top:0; left:0; right:0; height:52px; z-index:150;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 28px;
  background: rgba(2,6,8,0.92);
  border-bottom: 1px solid var(--c-border);
  backdrop-filter: blur(12px);
}
.logo-text {
  font-family: var(--font-display);
  font-size: 18px; font-weight: 900;
  color: var(--c-cyan);
  letter-spacing: 6px;
  text-shadow: 0 0 20px var(--c-cyan), 0 0 40px rgba(0,220,255,0.3);
}
.logo-sub {
  font-family: var(--font-mono);
  font-size: 9px; color: var(--c-text-dim);
  letter-spacing: 2px; margin-left: 14px;
}
.status-pill {
  display: flex; align-items: center; gap: 8px;
  background: rgba(0,220,255,0.06);
  border: 1px solid var(--c-border);
  border-radius: 20px; padding: 5px 16px;
  font-family: var(--font-display);
  font-size: 10px; letter-spacing: 3px;
}
.status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--c-ok);
  box-shadow: 0 0 8px var(--c-ok);
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

.hud-clock {
  font-family: var(--font-display); font-size: 20px; font-weight:700;
  color: var(--c-cyan); text-align: right;
  text-shadow: 0 0 12px var(--c-cyan);
}
.hud-date {
  font-family: var(--font-mono); font-size: 9px;
  color: var(--c-text-dim); text-align: right; letter-spacing: 2px;
}

/* ══════════ MAIN LAYOUT ══════════ */
.main-layout {
  position: fixed; top:52px; bottom:0; left:0; right:0;
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 0;
  padding: 12px;
  overflow: hidden;
}

/* ══════════ SIDE PANELS ══════════ */
.side-panel {
  display: flex; flex-direction: column; gap: 10px;
  overflow: hidden; padding: 4px;
}
.panel-card {
  background: var(--c-panel);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  padding: 14px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  transition: border-color .3s;
}
.panel-card::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, transparent, var(--c-cyan), transparent);
  opacity:.4;
}
.panel-card:hover { border-color: var(--c-border-hi); }

.card-header {
  display: flex; align-items: center; gap: 8px;
  font-family: var(--font-display); font-size: 9px;
  letter-spacing: 3px; color: var(--c-cyan);
  margin-bottom: 12px; text-transform: uppercase;
}
.card-icon { font-size: 14px; opacity:.7; }

/* ── Diagnostics ── */
.diag-grid { display: flex; flex-direction: column; gap: 8px; }
.diag-item { display:flex; align-items:center; gap:8px; }
.diag-label {
  font-family: var(--font-mono); font-size:9px;
  color: var(--c-text-dim); width:68px; flex-shrink:0;
}
.diag-bar-wrap {
  flex:1; height:4px; background:rgba(0,220,255,0.08);
  border-radius:2px; overflow:hidden;
  border: 1px solid rgba(0,220,255,0.1);
}
.diag-bar {
  height:100%; width:0%; border-radius:2px;
  background: linear-gradient(90deg, var(--c-blue), var(--c-cyan));
  box-shadow: 0 0 6px var(--c-cyan);
  transition: width 0.6s cubic-bezier(.4,0,.2,1);
}
.diag-bar.neural { background: linear-gradient(90deg, var(--c-purple), #cc44ff); box-shadow: 0 0 6px #cc44ff; }
.diag-bar.audio  { background: linear-gradient(90deg, #00ff88, #00ccaa); box-shadow: 0 0 6px #00ff88; }
.diag-val { font-family:var(--font-mono); font-size:9px; color:var(--c-cyan); width:28px; text-align:right; }

.metric-row { display:flex; gap:6px; margin-top:14px; }
.metric-box {
  flex:1; text-align:center;
  background: rgba(0,220,255,0.04);
  border: 1px solid var(--c-border);
  border-radius:3px; padding:8px 4px;
}
.metric-val { font-family:var(--font-display); font-size:11px; color:var(--c-cyan); }
.metric-lbl { font-family:var(--font-mono); font-size:8px; color:var(--c-text-dim); margin-top:3px; }

/* ── Tool List ── */
.tool-list { display:flex; flex-direction:column; gap:6px; }
.tool-item {
  display:flex; align-items:center; gap:8px;
  padding: 7px 10px;
  border-radius:3px;
  border: 1px solid transparent;
  transition: all .3s;
  background: rgba(0,220,255,0.02);
}
.tool-item.active {
  border-color: rgba(0,220,255,0.2);
  background: rgba(0,220,255,0.06);
}
.tool-item.firing {
  border-color: var(--c-cyan);
  background: rgba(0,220,255,0.12);
  box-shadow: 0 0 12px rgba(0,220,255,0.15);
}
.tool-dot {
  width:6px; height:6px; border-radius:50%;
  background: var(--c-text-dim);
  flex-shrink:0;
}
.tool-item.active .tool-dot { background:var(--c-ok); box-shadow:0 0 6px var(--c-ok); animation:blink 2s infinite; }
.tool-item.firing .tool-dot { background:var(--c-cyan); box-shadow:0 0 10px var(--c-cyan); animation:blink .4s infinite; }
.tool-name { font-family:var(--font-mono); font-size:9px; color:var(--c-text-mid); flex:1; letter-spacing:1px; }
.tool-status { font-family:var(--font-mono); font-size:8px; color:var(--c-text-dim); }
.tool-item.active .tool-status { color:var(--c-ok); }
.tool-item.firing .tool-status { color:var(--c-cyan); }

/* ── Waveform ── */
#waveformCanvas { width:100%; border-radius:3px; display:block; }

/* ══════════ CENTER CORE ══════════ */
.center-core {
  display: flex; flex-direction:column; align-items:center; justify-content:center; gap:20px;
  padding: 0 20px;
  position:relative;
}
.core-wrapper {
  position: relative; display:flex; flex-direction:column; align-items:center; gap:10px;
}
#coreCanvas {
  border-radius:50%;
  filter: drop-shadow(0 0 30px rgba(0,220,255,0.4));
  cursor:pointer;
}
.core-label {
  font-family: var(--font-display); font-size:14px; font-weight:700;
  color: var(--c-cyan); letter-spacing:6px;
  text-shadow: 0 0 20px var(--c-cyan);
  text-align:center;
}
.core-sublabel {
  font-family: var(--font-mono); font-size:10px;
  color: var(--c-text-dim); letter-spacing:2px; text-align:center;
}

/* ── Voice Controls ── */
.voice-controls { display:flex; flex-direction:column; align-items:center; gap:10px; }
.voice-btn {
  width:62px; height:62px; border-radius:50%;
  background: rgba(0,220,255,0.06);
  border: 2px solid var(--c-border-hi);
  color: var(--c-cyan); cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  transition: all .25s;
  position:relative; overflow:hidden;
}
.voice-btn svg { width:26px; height:26px; }
.voice-btn:hover {
  background: rgba(0,220,255,0.12);
  border-color: var(--c-cyan);
  box-shadow: 0 0 25px rgba(0,220,255,0.3), inset 0 0 15px rgba(0,220,255,0.05);
  transform: scale(1.05);
}
.voice-btn.listening {
  background: rgba(0,220,255,0.18);
  border-color: var(--c-cyan);
  box-shadow: 0 0 40px rgba(0,220,255,0.5), inset 0 0 20px rgba(0,220,255,0.1);
  animation: pulse-ring .8s ease-in-out infinite;
}
.voice-btn.processing {
  border-color: var(--c-warn);
  color: var(--c-warn);
  box-shadow: 0 0 30px rgba(255,170,0,0.4);
}
@keyframes pulse-ring {
  0%,100%{ box-shadow:0 0 30px rgba(0,220,255,.4); }
  50%{ box-shadow:0 0 55px rgba(0,220,255,.7); }
}
.voice-hint {
  font-family: var(--font-display); font-size:9px;
  color: var(--c-text-dim); letter-spacing:3px;
}

/* ── Text Input ── */
.text-input-row { display:flex; gap:8px; width:100%; max-width:460px; }
.nexus-input {
  flex:1; background:rgba(0,220,255,0.04);
  border: 1px solid var(--c-border);
  border-radius:3px; padding:10px 14px;
  color: var(--c-text); font-family:var(--font-mono); font-size:12px;
  outline:none; transition: border-color .3s, box-shadow .3s;
  letter-spacing:1px;
}
.nexus-input::placeholder { color:var(--c-text-dim); }
.nexus-input:focus {
  border-color: var(--c-cyan);
  box-shadow: 0 0 15px rgba(0,220,255,0.15);
}
.send-btn {
  background: rgba(0,220,255,0.1);
  border: 1px solid var(--c-cyan);
  color: var(--c-cyan); border-radius:3px;
  padding: 10px 18px;
  font-family: var(--font-display); font-size:9px; letter-spacing:2px;
  cursor:pointer; transition: all .25s;
}
.send-btn:hover {
  background:rgba(0,220,255,0.2);
  box-shadow: 0 0 15px rgba(0,220,255,0.25);
}

/* ══════════ CHAT HISTORY ══════════ */
.chat-card { flex:1; display:flex; flex-direction:column; overflow:hidden; min-height:0; }
.clear-btn {
  margin-left:auto; background:transparent; border:none;
  color:var(--c-text-dim); cursor:pointer; font-size:11px;
  transition:color .2s;
}
.clear-btn:hover { color:var(--c-cyan); }
.chat-history {
  flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:10px;
  padding-right:4px;
}
.chat-history::-webkit-scrollbar { width:3px; }
.chat-history::-webkit-scrollbar-track { background:transparent; }
.chat-history::-webkit-scrollbar-thumb { background:var(--c-border); border-radius:2px; }

.chat-msg { display:flex; gap:8px; animation: msgIn .35s ease; }
@keyframes msgIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }

.msg-avatar {
  width:26px; height:26px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:var(--font-display); font-size:10px; font-weight:700;
  flex-shrink:0; margin-top:2px;
}
.chat-msg.nexus .msg-avatar { background:rgba(0,220,255,0.12); color:var(--c-cyan); border:1px solid rgba(0,220,255,0.3); }
.chat-msg.user  .msg-avatar { background:rgba(0,102,255,0.12); color:#6699ff; border:1px solid rgba(0,102,255,0.3); }

.msg-content { flex:1; min-width:0; }
.msg-sender { font-family:var(--font-display); font-size:8px; letter-spacing:2px; color:var(--c-text-dim); display:block; margin-bottom:4px; }
.chat-msg.nexus .msg-sender { color:var(--c-cyan); }
.chat-msg.user  .msg-sender { color:#6699ff; }
.msg-content p {
  font-family:var(--font-body); font-size:12px; font-weight:300;
  color:var(--c-text); line-height:1.55;
  background:rgba(0,220,255,0.03); border:1px solid var(--c-border);
  border-radius:3px; padding:8px 10px;
}
.chat-msg.user .msg-content p { background:rgba(0,102,255,0.04); border-color:rgba(0,102,255,0.15); }
.msg-time { font-family:var(--font-mono); font-size:8px; color:var(--c-text-dim); margin-top:3px; display:block; }

/* ══════════ TERMINAL LOG ══════════ */
.terminal-card { flex-shrink:0; }
.terminal-blink { color:var(--c-ok); font-size:8px; margin-left:auto; animation:blink 1s infinite; }
.terminal-log {
  height:130px; overflow-y:auto; display:flex; flex-direction:column; gap:3px;
}
.terminal-log::-webkit-scrollbar { width:3px; }
.terminal-log::-webkit-scrollbar-thumb { background:var(--c-border); border-radius:2px; }
.t-line {
  font-family:var(--font-mono); font-size:9px;
  color:var(--c-text-dim); line-height:1.4; letter-spacing:.5px;
  animation: msgIn .2s ease;
}
.t-line.highlight { color:var(--c-cyan); }
.t-line.warn { color:var(--c-warn); }
.t-line.ok { color:var(--c-ok); }

/* ══════════ STATE TRANSITIONS ══════════ */
body.listening .status-dot  { background:var(--c-cyan); box-shadow:0 0 12px var(--c-cyan); animation:blink .4s infinite; }
body.processing .status-dot { background:var(--c-warn);  box-shadow:0 0 12px var(--c-warn);  animation:blink .3s infinite; }
body.speaking .status-dot   { background:var(--c-ok);    box-shadow:0 0 12px var(--c-ok);    animation:blink .6s infinite; }

/* ══════════ SCROLLBAR GLOBAL ══════════ */
* { scrollbar-width:thin; scrollbar-color:var(--c-border) transparent; }

/* ══════════ REDUCED MOTION ══════════ */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
'''

SPACE_CSS = '''/* ══════════ PRELOADER SPACE OPENING ══════════ */
.preloader {
  position: fixed;
  inset: 0;
  background: #000;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  opacity: 1;
  transition: opacity 1.5s ease-out;
}
.preloader.fade-out {
  opacity: 0;
  pointer-events: none;
}
.starfield {
  position: absolute;
  inset: 0;
  background: transparent;
  pointer-events: none;
}
.starfield::before {
  content: "";
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background:
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.8) 0px, transparent 10%),
    radial-gradient(circle at 80% 70%, rgba(255,255,255,0.6) 0px, transparent 10%),
    radial-gradient(circle at 40% 60%, rgba(255,255,255,0.4) 0px, transparent 10%),
    radial-gradient(circle at 70% 50%, rgba(255,255,255,0.3) 0px, transparent 10%);
  animation: moveStars 60s linear infinite;
  background-size: 200% 200%;
}
@keyframes moveStars {
  0% { background-position: 0 0; }
  100% { background-position: -200% -200%; }
}
.nebula {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 30%, rgba(0, 100, 255, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 70% 70%, rgba(100, 0, 255, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(0, 200, 255, 0.1) 0%, transparent 50%);
  animation: nebulaPulse 8s ease-in-out infinite;
  pointer-events: none;
}
@keyframes nebulaPulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}
.loading-text {
  position: relative;
  font-family: 'Orbitron', monospace;
  font-size: 1.5rem;
  letter-spacing: 4px;
  color: #00dcff;
  text-shadow: 0 0 10px #00dcff, 0 0 20px rgba(0,220,255,0.3);
  animation: textPulse 2s ease-in-out infinite;
  z-index: 2;
}
@keyframes textPulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}'''

APP_JS = '''/**
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
  msg.className = 'chat-msg ' + (role === 'nexus' ? 'nexus' : 'user');
  const timeStr = new Date().toTimeString().slice(0,8);
  msg.innerHTML = `
    <div class="msg-avatar">${role === 'nexus' ? 'N' : 'U'}</div>
    <div class="msg-content">
      <span class="msg-sender">${role === 'nexus' ? 'NEXUS' : 'YOU'}</span>
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
    addMessage('nexus', reply);
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
- For greetings, respond in character as NEXUS
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
  addMessage('nexus', reply);
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
'''

FAVICON_ICO = ''

FAVICON_PNG = ''

