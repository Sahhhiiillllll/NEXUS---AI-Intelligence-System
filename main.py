"""
J.A.R.V.I.S — main.py
======================
Async orchestration entry point.

Starts:
  1. WebSocket server (serves frontend on ws://host:port)
  2. HTTP server for health checks and metrics (on http://host:http_port)
  3. AudioEngine for mic capture
  4. Routes all queries through the IntentRouter

Usage:
    python main.py
"""

import asyncio
import json
import signal
import sys
import time
import websockets
from aiohttp import web

from audio_engine import AudioEngine
from intents     import IntentRouter
from logger      import get_logger
from config      import get_config
from health      import get_health_checker
from metrics     import get_metrics

# Get configuration
config = get_config()
log = get_logger("main")


class JarvisCore:
    """
    Central coordinator.
    Manages WebSocket clients and orchestrates the full pipeline:
    AudioEngine → IntentRouter → response → TTS + WS broadcast
    """

    def __init__(self):
        self.router         = IntentRouter()
        self.audio          = AudioEngine(on_transcript=self._handle_transcript)
        self.ws_clients: set = set()
        self._running       = True
        log.info("JarvisCore initialized", extra={"event": "boot"})

    # ─────────────── WebSocket server ───────────────
    async def ws_handler(self, websocket):
        """Handle a single WebSocket client."""
        self.ws_clients.add(websocket)
        client_ip = websocket.remote_address[0]
        log.info(f"Client connected: {client_ip}", extra={"event": "ws_connect"})
        try:
            async for raw in websocket:
                try:
                    data = json.loads(raw)
                    if data.get("type") == "query":
                        await self._process_query(data["text"], websocket)
                except json.JSONDecodeError:
                    log.warning("Invalid JSON from client", extra={"raw": raw[:80]})
        except websockets.exceptions.ConnectionClosedOK:
            pass
        except Exception as e:
            log.error(f"WS error: {e}", extra={"event": "ws_error"})
        finally:
            self.ws_clients.discard(websocket)
            log.info(f"Client disconnected: {client_ip}", extra={"event": "ws_disconnect"})

    async def broadcast(self, payload: dict):
        """Send payload to every connected WebSocket client."""
        if not self.ws_clients:
            return
        message = json.dumps(payload)
        await asyncio.gather(
            *[client.send(message) for client in list(self.ws_clients)],
            return_exceptions=True,
        )

    # ─────────────── Query pipeline ───────────────
    async def _process_query(self, text: str, ws=None):
        """Full pipeline: classify → tool → respond → TTS."""
        log.info(f"Processing query: {text[:60]}", extra={"event": "query", "text": text})
        t0 = time.perf_counter()

        # Notify frontend: processing started
        await self.broadcast({"type": "state", "state": "PROCESSING"})

        try:
            result = await self.router.route(text)
        except Exception as e:
            log.error(f"Router error: {e}", extra={"event": "router_error"})
            result = {
                "response": "I encountered an unexpected error. Please try again.",
                "tool":     "llm",
                "log":      f"Error: {str(e)[:80]}",
            }

        elapsed_ms = round((time.perf_counter() - t0) * 1000)
        result["latency_ms"] = elapsed_ms
        result["type"]       = "response"

        log.info(f"Response ready in {elapsed_ms}ms", extra={"event": "response", "ms": elapsed_ms})

        # Broadcast full response to frontend
        await self.broadcast(result)

        # Speak the response (non-blocking)
        response_text = result.get("response", "")
        if response_text:
            asyncio.create_task(self.audio.speak_async(response_text))

    async def _handle_transcript(self, text: str):
        """Called by AudioEngine when mic captures a final transcript."""
        await self.broadcast({"type": "transcript", "text": text})
        await self._process_query(text)

    # ─────────────── HTTP server handlers ───────────────
    async def health_live_handler(self, request):
        """Liveness probe endpoint."""
        health_checker = get_health_checker()
        body, status_code = health_checker.check_liveness()
        return web.json_response(body, status=status_code)

    async def health_ready_handler(self, request):
        """Readiness probe endpoint."""
        health_checker = get_health_checker()
        body, status_code = health_checker.check_readiness()
        return web.json_response(body, status=status_code)

    async def health_deep_handler(self, request):
        """Deep health check endpoint."""
        health_checker = get_health_checker()
        body, status_code = health_checker.check_deep()
        return web.json_response(body, status=status_code)

    async def metrics_handler(self, request):
        """Prometheus metrics endpoint."""
        metrics_data, content_type = get_metrics()
        return web.Response(body=metrics_data, content_type=content_type)

    # ─────────────── Lifecycle ───────────────
    async def run(self):
        """Start all subsystems."""
        # Validate configuration on startup
        if not config.validate_config():
            log.error("Configuration validation failed. Please check your settings.")
            sys.exit(1)

        log.info(f"Starting WebSocket server on ws://{config.server.host}:{config.server.port}",
                extra={"event": "boot"})

        # Start HTTP server for health checks and metrics
        http_app = web.Application()
        http_app.router.add_get('/health/live', self.health_live_handler)
        http_app.router.add_get('/health/ready', self.health_ready_handler)
        http_app.router.add_get('/health/deep', self.health_deep_handler)
        http_app.router.add_get('/metrics', self.metrics_handler)

        http_runner = web.AppRunner(http_app)
        await http_runner.setup()
        http_site = web.TCPSite(http_runner, config.server.host, config.server.port + 1000)  # HTTP on port+1000
        await http_site.start()
        log.info(f"HTTP server started on http://{config.server.host}:{config.server.port + 1000}",
                extra={"event": "http_server_start"})

        # Start WS server
        ws_server = await websockets.serve(
            self.ws_handler,
            config.server.host,
            config.server.port
        )

        # Start audio engine in background
        audio_task = asyncio.create_task(self.audio.listen_loop())

        log.info("J.A.R.V.I.S is online", extra={"event": "ready"})
        print("\n" + "═" * 60)
        print("  J.A.R.V.I.S — Unified Intelligence Core")
        print(f"  WebSocket: ws://{config.server.host}:{config.server.port}")
        print(f"  HTTP:      http://{config.server.host}:{config.server.port + 1000}")
        print("  Open public/index.html in a browser")
        print("═" * 60 + "\n")

        try:
            await asyncio.Future()  # run forever
        except asyncio.CancelledError:
            pass
        finally:
            self._running = False
            audio_task.cancel()
            ws_server.close()
            await ws_server.wait_closed()
            await http_runner.cleanup()
            log.info("Shutdown complete", extra={"event": "shutdown"})


def main():
    core = JarvisCore()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def _shutdown(*_):
        print("\n[JARVIS] Shutdown signal received...")
        for task in asyncio.all_tasks(loop):
            task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _shutdown)
        except NotImplementedError:
            pass  # Windows fallback

    try:
        loop.run_until_complete(core.run())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()