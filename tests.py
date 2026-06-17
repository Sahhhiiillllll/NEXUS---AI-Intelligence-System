"""
J.A.R.V.I.S — tests.py
=======================
Unit tests for all backend modules.

Run:
    python -m pytest tests.py -v
    # or
    python tests.py
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# ── Add backend to path ──
sys.path.insert(0, os.path.dirname(__file__))

from intents import (
    IntentRouter, LLMTool, WolframTool, WeatherTool,
    WebSearchTool, SchedulerTool, FallbackTool,
)
from logger import get_logger

log = get_logger("tests")


def run_async(coro):
    """Helper to run an async coroutine in tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ═══════════════════════════════ FALLBACK TOOL ═══════════════════════════════
class TestFallbackTool(unittest.TestCase):

    def setUp(self):
        self.tool = FallbackTool()

    def test_greeting(self):
        result = self.tool.run_sync("Hello there!")
        self.assertIn("service", result["response"].lower())
        self.assertEqual(result["tool"], "llm")

    def test_thanks(self):
        result = self.tool.run_sync("Thank you very much")
        self.assertIn("pleasure", result["response"].lower() + result["response"])

    def test_identity(self):
        result = self.tool.run_sync("Who are you?")
        self.assertIn("J.A.R.V.I.S", result["response"])

    def test_unknown(self):
        result = self.tool.run_sync("xyzzy quux undefined gibberish 12345")
        self.assertIsInstance(result["response"], str)
        self.assertTrue(len(result["response"]) > 5)

    def test_returns_dict_keys(self):
        result = self.tool.run_sync("hi")
        self.assertIn("response", result)
        self.assertIn("tool",     result)
        self.assertIn("log",      result)


# ═══════════════════════════════ SCHEDULER TOOL ══════════════════════════════
class TestSchedulerTool(unittest.TestCase):

    def setUp(self):
        self.tool = SchedulerTool()
        SchedulerTool._reminders = []  # reset between tests

    def test_time_query(self):
        result = run_async(self.tool.run("What time is it?", []))
        self.assertIn("time", result["response"].lower())
        self.assertIn("AM", result["response"] + "PM")

    def test_date_query(self):
        result = run_async(self.tool.run("What is today's date?", []))
        self.assertIn("today", result["response"].lower() + result["log"].lower())

    def test_set_reminder(self):
        result = run_async(self.tool.run("Remind me to call Alice at 3:00 PM", []))
        self.assertIn("call Alice", result["response"])
        self.assertEqual(len(SchedulerTool._reminders), 1)

    def test_list_reminders_empty(self):
        result = run_async(self.tool.run("Show my reminders", []))
        self.assertIn("no active", result["response"].lower())

    def test_list_reminders_with_items(self):
        SchedulerTool._reminders.append({"task": "buy milk", "when": "5pm", "set_at": "now"})
        result = run_async(self.tool.run("List my reminders", []))
        self.assertIn("buy milk", result["response"])


# ═══════════════════════════════ INTENT ROUTER ═══════════════════════════════
class TestIntentRouter(unittest.TestCase):

    def setUp(self):
        self.router = IntentRouter()

    def test_classify_weather(self):
        self.assertEqual(self.router.classify("What's the weather in London?"), "weather")

    def test_classify_wolfram(self):
        self.assertEqual(self.router.classify("Calculate the integral of x squared"), "wolfram")

    def test_classify_scheduler_time(self):
        self.assertEqual(self.router.classify("What time is it?"), "scheduler")

    def test_classify_scheduler_reminder(self):
        self.assertEqual(self.router.classify("Remind me to take medicine"), "scheduler")

    def test_classify_search(self):
        self.assertEqual(self.router.classify("Search for the latest news"), "search")

    def test_classify_llm_fallback(self):
        self.assertEqual(self.router.classify("Tell me a bedtime story"), "llm")

    def test_classify_case_insensitive(self):
        self.assertEqual(self.router.classify("WEATHER IN PARIS"), "weather")

    def test_context_grows(self):
        async def _go():
            with patch.object(FallbackTool, 'run', new_callable=AsyncMock,
                               return_value={"response": "Hi", "tool": "llm", "log": "ok"}):
                with patch.object(LLMTool, 'run', new_callable=AsyncMock,
                                  return_value={"response": "Hi", "tool": "llm", "log": "ok"}):
                    await self.router.route("Hello")
                    await self.router.route("What's up?")
        run_async(_go())
        self.assertGreater(len(self.router._context), 0)

    def test_context_truncated(self):
        """Context should not grow beyond MAX_HISTORY * 2 entries."""
        async def _go():
            with patch.object(LLMTool, 'run', new_callable=AsyncMock,
                               return_value={"response": "ok", "tool": "llm", "log": "ok"}):
                for _ in range(30):
                    await self.router.route("Tell me something")
        run_async(_go())
        self.assertLessEqual(len(self.router._context), self.router.MAX_HISTORY * 2)


# ═══════════════════════════════ WEATHER TOOL ════════════════════════════════
class TestWeatherTool(unittest.TestCase):

    def setUp(self):
        self.tool = WeatherTool()

    def test_extract_city_in(self):
        city = WeatherTool._extract_city("What's the weather in Tokyo?")
        self.assertEqual(city, "Tokyo")

    def test_extract_city_for(self):
        city = WeatherTool._extract_city("Get forecast for Berlin")
        self.assertEqual(city, "Berlin")

    def test_extract_city_none(self):
        city = WeatherTool._extract_city("Is it raining?")
        self.assertIsNone(city)

    def test_no_api_key_graceful(self):
        """Without API key, should return a graceful message, not raise."""
        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": ""}):
            # Temporarily clear the module-level variable
            import intents as _intents
            orig = _intents.OPENWEATHER_API_KEY
            _intents.OPENWEATHER_API_KEY = ""
            try:
                result = run_async(self.tool.run("weather in Paris", []))
                self.assertIn("key", result["response"].lower() + result["log"].lower())
            finally:
                _intents.OPENWEATHER_API_KEY = orig

    def test_live_api_mock(self):
        """Mock aiohttp to verify correct API call and response parsing."""
        mock_data = {
            "main":    {"temp": 22.3, "feels_like": 21.0, "humidity": 65},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "wind":    {"speed": 4.2},
        }

        async def _go():
            with patch("aiohttp.ClientSession") as mock_session_cls:
                mock_resp = AsyncMock()
                mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
                mock_resp.__aexit__  = AsyncMock(return_value=False)
                mock_resp.status    = 200
                mock_resp.json      = AsyncMock(return_value=mock_data)

                mock_get = AsyncMock()
                mock_get.__aenter__ = AsyncMock(return_value=mock_resp)
                mock_get.__aexit__  = AsyncMock(return_value=False)

                mock_session = AsyncMock()
                mock_session.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session.__aexit__  = AsyncMock(return_value=False)
                mock_session.get        = MagicMock(return_value=mock_get)

                mock_session_cls.return_value = mock_session

                import intents as _intents
                _intents.OPENWEATHER_API_KEY = "test_key"

                result = await self.tool.run("weather in London", [])
                self.assertIn("22", result["response"])
                self.assertIn("clear sky", result["response"].lower())

        run_async(_go())


# ═══════════════════════════════ LLM TOOL ════════════════════════════════════
class TestLLMTool(unittest.TestCase):

    def test_no_api_key_returns_fallback(self):
        import intents as _intents
        orig = _intents.OPENROUTER_API_KEY
        _intents.OPENROUTER_API_KEY = ""
        try:
            result = run_async(LLMTool().run("Hello", []))
            self.assertIsInstance(result["response"], str)
            self.assertTrue(len(result["response"]) > 5)
        finally:
            _intents.OPENROUTER_API_KEY = orig

    def test_api_mock_success(self):
        mock_response = {
            "choices": [{"message": {"content": "I am JARVIS, at your service."}}]
        }

        async def _go():
            with patch("aiohttp.ClientSession") as mock_session_cls:
                mock_resp = AsyncMock()
                mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
                mock_resp.__aexit__  = AsyncMock(return_value=False)
                mock_resp.json       = AsyncMock(return_value=mock_response)

                mock_post = AsyncMock()
                mock_post.__aenter__ = AsyncMock(return_value=mock_resp)
                mock_post.__aexit__  = AsyncMock(return_value=False)

                mock_session = AsyncMock()
                mock_session.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session.__aexit__  = AsyncMock(return_value=False)
                mock_session.post       = MagicMock(return_value=mock_post)

                mock_session_cls.return_value = mock_session

                import intents as _intents
                _intents.OPENROUTER_API_KEY = "sk-or-test-key"

                result = await LLMTool().run("Hello", [])
                self.assertIn("JARVIS", result["response"])

        run_async(_go())


# ═══════════════════════════════ LOGGER ══════════════════════════════════════
class TestLogger(unittest.TestCase):

    def test_logger_returns_logger(self):
        logger = get_logger("test")
        self.assertIsNotNone(logger)

    def test_logger_name(self):
        logger = get_logger("mymodule")
        self.assertEqual(logger.name, "jarvis.mymodule")

    def test_json_log_file_created(self):
        from logger import LOG_FILE
        logger = get_logger("file_test")
        logger.info("Test log entry", extra={"event": "unit_test"})
        self.assertTrue(LOG_FILE.exists())

    def test_json_log_parseable(self):
        from logger import LOG_FILE
        logger = get_logger("json_test")
        logger.info("JSON parse test", extra={"event": "test", "value": 42})
        with open(LOG_FILE) as f:
            lines = f.readlines()
        # At least one line should be valid JSON
        last = json.loads(lines[-1])
        self.assertIn("message", last)
        self.assertIn("level",   last)
        self.assertIn("ts",      last)


# ═══════════════════════════════ ENTRY POINT ═════════════════════════════════
if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  J.A.R.V.I.S Unit Test Suite")
    print("═" * 60 + "\n")
    unittest.main(verbosity=2)
