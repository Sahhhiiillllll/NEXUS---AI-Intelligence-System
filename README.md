# J.A.R.V.I.S — Unified Intelligence Core

> **J.A.R.V.I.S** (Just A Rather Very Intelligent System) is a production-ready, voice-enabled AI assistant inspired by Tony Stark's AI from the Iron Man franchise. It ships with a cyberpunk neural HUD, real-time voice interaction, multi-tool LLM routing, and **one-click Vercel deployment** where the Python API starts automatically with the app — no separate backend server to run.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Requirements](#requirements)
4. [Dependencies](#dependencies)
5. [Installation](#installation)
6. [How to Use](#how-to-use)
7. [Deployment on Vercel (Recommended)](#deployment-on-vercel-recommended)
8. [Local Development Modes](#local-development-modes)
9. [Docker Deployment](#docker-deployment)
10. [Environment Variables](#environment-variables)
11. [API Endpoints](#api-endpoints)
12. [Monitoring & Health Checks](#monitoring--health-checks)
13. [Project Structure](#project-structure)
14. [Troubleshooting](#troubleshooting)
15. [License](#license)

---

## Features

| Category | Capabilities |
|----------|-------------|
| **Voice UI** | Web Speech API (STT + TTS), waveform visualizer, Arc Reactor HUD |
| **AI Brain** | OpenRouter LLM (Claude) via intent router with conversation memory |
| **Tools** | Weather (OpenWeatherMap), Wolfram Alpha, DuckDuckGo search, scheduler |
| **Resilience** | Circuit breakers, retry with backoff, bulkhead isolation |
| **Observability** | Structured JSON logging, Prometheus metrics (local mode), health probes |
| **Deployment** | Vercel serverless (frontend + API unified), Docker, local WebSocket |

---

## Architecture

### Production (Vercel) — Unified Stack

On Vercel, opening the app **automatically** activates the Python backend. There is no separate process to start — Vercel serverless functions spin up on demand when you send a chat message.

```
┌─────────────────────────────────────────────────────────────────┐
│                     VERCEL (single deployment)                   │
│                                                                  │
│  Browser ──► Static Frontend (frontend/)                        │
│                  │                                               │
│                  │  POST /api/chat  (auto-starts Python)        │
│                  ▼                                               │
│            api/index.py  (FastAPI serverless)                   │
│                  │                                               │
│                  ▼                                               │
│            IntentRouter ──► LLM / Weather / Wolfram / Search      │
└─────────────────────────────────────────────────────────────────┘
```

### Local Full-Stack (WebSocket + Audio)

For development with microphone capture and persistent WebSocket:

```
┌─────────────────┐    WebSocket     ┌──────────────────┐
│   Frontend UI   │ ◀──────────────▶ │   main.py        │
│  (HTML/CSS/JS)  │   ws://:8765     │  JarvisCore      │
└─────────────────┘                  └────────┬─────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
              IntentRouter              AudioEngine                 HTTP :9765
              (tool plugins)         (mic + pyttsx3)            health/metrics
```

### Core Modules

| Module | Role |
|--------|------|
| `frontend/` | Neural HUD UI — canvas animations, chat, voice controls |
| `api/index.py` | Vercel serverless FastAPI entry (production API) |
| `main.py` | Local async orchestrator (WebSocket + audio + HTTP) |
| `intents.py` | Intent classification and tool routing |
| `resilient.py` | Circuit breaker, retry, bulkhead patterns |
| `config.py` | Pydantic settings from environment variables |
| `audio_engine.py` | Local microphone + TTS (not used on Vercel) |
| `health.py` / `metrics.py` | Probes and Prometheus (local mode) |

---

## Requirements

### Runtime

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | 3.9+ (3.11 recommended) | Backend & Vercel functions |
| **Node.js** | 18+ | Vercel CLI & build orchestration only |
| **Git** | Any recent | Clone & deploy |
| **Vercel account** | Free tier works | For production hosting |

### API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `OPENROUTER_API_KEY` | **Yes** (for LLM) | Primary AI brain via [OpenRouter](https://openrouter.ai/) |
| `WOLFRAM_APP_ID` | No | Math/science queries |
| `OPENWEATHER_API_KEY` | No | Live weather |
| `JARVIS_DEMO_MODE=true` | No | Offline fallback responses |

### System (local audio mode only)

- **macOS:** `brew install portaudio`
- **Ubuntu/Debian:** `sudo apt install portaudio19-dev python3-pyaudio`
- **Windows:** PyAudio wheels via pip

---

## Dependencies

### Production / Vercel (`requirements.txt`)

```
aiohttp>=3.9.0          # Async HTTP client for external APIs
fastapi>=0.100.0        # Serverless API framework
uvicorn>=0.23.2         # ASGI server (local testing)
pydantic>=2.0.0         # Config validation
python-dotenv>=1.0.0    # .env loading
prometheus-client>=0.17.0
pytest>=8.0.0           # Tests
pytest-asyncio>=0.23.0
websockets>=12.0        # Local WebSocket server
```

### Local Full-Stack (`requirements-local.txt`)

Includes everything above **plus**:

```
pyaudio>=0.2.11
SpeechRecognition>=3.10.0
pyttsx3>=2.90
```

Install:

```bash
# Vercel / serverless only
pip install -r requirements.txt

# Local with microphone + WebSocket
pip install -r requirements-local.txt
```

---

## Installation

### 1. Clone

```bash
git clone https://github.com/Sahhhiiillllll/JARVIS---AI-Intelligence-System-LLM.git
cd JARVIS---AI-Intelligence-System-LLM
```

### 2. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements-local.txt
```

### 3. Configure secrets

```bash
cp .env.example .env
# Edit .env — add your OPENROUTER_API_KEY at minimum
```

### 4. Verify

```bash
python -c "from intents import IntentRouter; print('Backend OK')"
```

---

## How to Use

1. **Deploy to Vercel** (see below) or run locally.
2. Open the app URL in **Chrome, Edge, or Safari** (best Web Speech API support).
3. Wait for the boot sequence to finish.
4. **Speak:** click the Arc Reactor core or microphone button.
5. **Type:** use the text input and press **SEND** or **Enter**.
6. JARVIS routes your query to the right tool and responds via chat + TTS.

### Example queries

| Query | Tool |
|-------|------|
| "Hello JARVIS" | LLM greeting |
| "What's the weather in London?" | Weather |
| "Integrate x squared from 0 to 5" | Wolfram |
| "Who is Elon Musk?" | Web search |
| "Set a timer for 10 minutes" | Scheduler |

---

## Deployment on Vercel (Recommended)

This is the **production-ready** path. Frontend and Python API deploy together — the backend runs automatically when users interact with the app.

### Option A: One-Click Deploy

1. Click **Deploy with Vercel** button above (or import the GitHub repo in [vercel.com/new](https://vercel.com/new)).
2. Add environment variables in the Vercel dashboard:

   | Variable | Value |
   |----------|-------|
   | `OPENROUTER_API_KEY` | Your OpenRouter key |
   | `OPENROUTER_MODEL` | (optional) e.g. `anthropic/claude-sonnet-4` |
   | `WOLFRAM_APP_ID` | (optional) |
   | `OPENWEATHER_API_KEY` | (optional) |
   | `JARVIS_CITY` | Default city, e.g. `New York` |

3. Deploy. Vercel will:
   - Serve `frontend/` as static files
   - Auto-detect `api/index.py` as Python serverless functions
   - Install `requirements.txt` on each function cold start

### Option B: Vercel CLI

```bash
npm install -g vercel
vercel login
vercel          # preview
vercel --prod   # production
```

Set env vars:

```bash
vercel env add OPENROUTER_API_KEY
vercel env add WOLFRAM_APP_ID
vercel env add OPENWEATHER_API_KEY
```

### How auto-start works

| User action | What happens |
|-------------|--------------|
| Opens app URL | Static HUD loads instantly from CDN |
| Sends first message | Vercel cold-starts `api/index.py` (FastAPI) |
| Subsequent messages | Function reuses warm instance when possible |
| Health check | `GET /api/health` confirms API is online |

The frontend detects non-localhost hosting and uses `fetch('/api/chat')` instead of WebSocket — **no manual server start required**.

### `vercel.json` summary

```json
{
  "outputDirectory": "frontend",
  "installCommand": "pip install -r requirements.txt",
  "rewrites": [{ "source": "/api/(.*)", "destination": "/api/index.py" }]
}
```

### Production checklist

- [ ] `OPENROUTER_API_KEY` set in Vercel Environment Variables (Production)
- [ ] Never commit `.env` to git
- [ ] Test `/api/health` after deploy
- [ ] Test a chat message end-to-end
- [ ] Optional: add custom domain in Vercel project settings

---

## Local Development Modes

### Mode 1: Vercel-like (recommended for testing deploy)

```bash
vercel dev
```

Opens frontend + serverless API locally at `http://localhost:3000`.

### Mode 2: Full WebSocket + Audio

```bash
# Terminal 1 — backend
python main.py

# Terminal 2 — frontend
python -m http.server 8080 --directory frontend
```

Open `http://localhost:8080` — connects via `ws://localhost:8765`.

### Mode 3: Makefile shortcuts

```bash
make dev                  # python main.py
make test                 # pytest tests.py -v
make docker-compose-up    # Docker stack
```

---

## Docker Deployment

For VPS / cloud containers with full WebSocket + audio:

```bash
docker build -t jarvis-ai .
docker run -d \
  --name jarvis \
  -p 8765:8765 \
  -p 9765:9765 \
  --env-file .env \
  jarvis-ai
```

Or with Compose:

```bash
docker-compose up -d
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key | — | Yes (LLM) |
| `OPENROUTER_MODEL` | Model routed via OpenRouter | `anthropic/claude-sonnet-4` | No |
| `WOLFRAM_APP_ID` | Wolfram Alpha App ID | — | No |
| `OPENWEATHER_API_KEY` | OpenWeatherMap key | — | No |
| `JARVIS_HOST` | WebSocket bind host (local) | `localhost` | No |
| `JARVIS_PORT` | WebSocket port (local) | `8765` | No |
| `JARVIS_DEBUG` | Verbose logging | `false` | No |
| `JARVIS_DEMO_MODE` | Offline fallback mode | `false` | No |
| `JARVIS_CITY` | Default weather city | `New York` | No |
| `JARVIS_HTTP_TIMEOUT` | HTTP timeout (seconds) | `15` | No |
| `JARVIS_MAX_RETRIES` | API retry count | `3` | No |
| `JARVIS_FAILURE_THRESHOLD` | Circuit breaker threshold | `5` | No |
| `JARVIS_ENABLE_METRICS` | Prometheus (local) | `true` | No |

---

## API Endpoints

### Vercel (serverless)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check — confirms API is online |
| `POST` | `/api/chat` | Send query, receive AI response |

**Request:**

```json
{ "text": "What's the weather in Tokyo?" }
```

**Response:**

```json
{
  "response": "The current temperature in Tokyo is...",
  "tool": "weather",
  "log": "OpenWeatherMap query succeeded",
  "type": "response",
  "latency_ms": 842
}
```

### Local (`main.py`)

| Path | Description |
|------|-------------|
| `ws://host:8765` | WebSocket — `{ "type": "query", "text": "..." }` |
| `GET /health/live` | Liveness probe |
| `GET /health/ready` | Readiness probe |
| `GET /health/deep` | Deep dependency check |
| `GET /metrics` | Prometheus metrics |

---

## Monitoring & Health Checks

**Vercel:** `curl https://your-app.vercel.app/api/health`

**Local:**

```bash
curl http://localhost:9765/health/live
curl http://localhost:9765/metrics
```

---

## Project Structure

```
JARVIS---AI-Intelligence-System-LLM/
├── api/
│   └── index.py           # Vercel serverless FastAPI (auto-starts)
├── frontend/
│   ├── index.html         # Neural HUD UI
│   ├── app.js             # Voice, chat, API client
│   ├── style.css
│   └── space.css
├── main.py                # Local WebSocket orchestrator
├── intents.py             # Intent router + tool plugins
├── resilient.py           # Circuit breaker / retry
├── config.py              # Settings
├── audio_engine.py        # Local mic + TTS
├── health.py              # Health probes
├── metrics.py             # Prometheus
├── requirements.txt       # Vercel / production deps
├── requirements-local.txt # + audio deps for local
├── vercel.json            # Vercel deployment config
├── package.json           # Vercel build scripts
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API returns 500 on Vercel | Check `OPENROUTER_API_KEY` in Vercel env vars |
| "Backend not reachable" | Wait for cold start; retry first message |
| Voice not working | Use HTTPS (Vercel provides this); allow mic permission |
| WebSocket fails locally | Run `python main.py` first; check port 8765 |
| PyAudio install fails | Install PortAudio system library (see Requirements) |
| CORS errors | Use `vercel dev` or serve frontend via HTTP, not `file://` |

---




