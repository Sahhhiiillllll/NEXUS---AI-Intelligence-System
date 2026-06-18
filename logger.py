"""
J.A.R.V.I.S — logger.py
========================
Structured JSON logging system.

Every log entry is a JSON object written to:
  - stderr (human-readable with color)
  - logs/jarvis.jsonl (machine-readable, one JSON object per line)

Frontend terminal reads logs/jarvis.jsonl via WebSocket broadcast from main.py.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib  import Path

# Use /tmp/logs for writable logs in serverless environments like Vercel
LOG_DIR  = Path("/tmp") / "logs"
LOG_FILE = LOG_DIR / "jarvis.jsonl"


class JSONFormatter(logging.Formatter):
    """Format log records as compact JSON lines."""

    LEVEL_COLORS = {
        "DEBUG":    "\033[36m",   # cyan
        "INFO":     "\033[32m",   # green
        "WARNING":  "\033[33m",   # yellow
        "ERROR":    "\033[31m",   # red
        "CRITICAL": "\033[35m",   # magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts":      datetime.now(timezone.utc).isoformat(),
            "level":   record.levelname,
            "logger":  record.name,
            "message": record.getMessage(),
        }
        # Merge any extra fields
        for key, val in record.__dict__.items():
            if key not in {
                "name","msg","args","levelname","levelno","pathname","filename",
                "module","exc_info","exc_text","stack_info","lineno","funcName",
                "created","msecs","relativeCreated","thread","threadName",
                "processName","process","message","taskName",
            }:
                entry[key] = val

        return json.dumps(entry, default=str)


class ColorConsoleFormatter(logging.Formatter):
    """Human-readable colored console output."""

    FMT = "{color}[{level:8s}]{reset} {ts} {logger:12s} {msg}"

    LEVEL_COLORS = {
        "DEBUG":    "\033[36m",
        "INFO":     "\033[32m",
        "WARNING":  "\033[33m",
        "ERROR":    "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelname, "")
        ts    = datetime.now().strftime("%H:%M:%S.%f")[:12]
        return self.FMT.format(
            color=color, level=record.levelname,
            reset=self.RESET, ts=ts,
            logger=record.name[:12], msg=record.getMessage(),
        )


def _setup_root_logger():
    """Configure root logger once."""
    root = logging.getLogger("jarvis")
    if root.handlers:
        return  # already configured

    root.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.INFO)
    ch.setFormatter(ColorConsoleFormatter())
    root.addHandler(ch)

    # File handler (JSON lines)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(JSONFormatter())
    root.addHandler(fh)

    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a named child logger under 'jarvis.*'."""
    _setup_root_logger()
    return logging.getLogger(f"jarvis.{name}")
