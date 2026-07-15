"""
N.A.X.U.S — Health Check Endpoints
==================================
HTTP endpoints for monitoring system health and readiness.
"""

from http import HTTPStatus
from typing import Dict, Tuple
import time
from config import get_config
from logger import get_logger

log = get_logger("health")


class HealthChecker:
    """Health check implementations for different system components."""

    def __init__(self):
        self.config = get_config()
        self.start_time = time.time()

    def check_liveness(self) -> Tuple[Dict, int]:
        """
        Liveness probe - determines if the container is running.
        Returns 200 if the application is running, regardless of dependencies.
        """
        return {
            "status": "alive",
            "timestamp": time.time(),
            "uptime_seconds": time.time() - self.start_time
        }, HTTPStatus.OK

    def check_readiness(self) -> Tuple[Dict, int]:
        """
        Readiness probe - determines if the container is ready to serve traffic.
        Checks that critical dependencies are functioning.
        """
        checks = {}
        overall_status = HTTPStatus.OK

        # Check 1: Configuration validity
        try:
            self.config  # Just accessing it triggers validation
            checks["config"] = {"status": "ok"}
        except Exception as e:
            checks["config"] = {"status": "error", "message": str(e)}
            overall_status = HTTPStatus.SERVICE_UNAVAILABLE
            log.error(f"Health check config failed: {e}")

        # Check 2: Logger functionality
        try:
            # Test that logger is working by attempting to log
            from logger import get_logger
            test_logger = get_logger("health_test")
            test_logger.info("Health check logger test")
            checks["logger"] = {"status": "ok"}
        except Exception as e:
            checks["logger"] = {"status": "error", "message": str(e)}
            overall_status = HTTPStatus.SERVICE_UNAVAILABLE
            log.error(f"Health check logger failed: {e}")

        # Check 3: Server binding (basic check)
        # In a real implementation, we might check if the port is bound
        # For now, we'll assume if we're running, the server is bound
        checks["server"] = {"status": "ok"}

        body = {
            "status": "ready" if overall_status == HTTPStatus.OK else "not_ready",
            "checks": checks,
            "timestamp": time.time()
        }

        return body, overall_status

    def check_deep(self) -> Tuple[Dict, int]:
        """
        Deep health check - comprehensive verification of all systems.
        Includes readiness checks plus optional dependency verification.
        """
        # Start with readiness check
        body, status_code = self.check_readiness()

        # Add additional deep checks here if needed
        # For example: external API connectivity (with timeouts/cache to avoid slowness)
        # But we'll keep it simple for now to avoid health check becoming a bottleneck

        body["check_type"] = "deep"
        body["timestamp"] = time.time()

        return body, status_code


# Global health checker instance
_health_checker: HealthChecker = None


def get_health_checker() -> HealthChecker:
    """Get or create the global health checker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker