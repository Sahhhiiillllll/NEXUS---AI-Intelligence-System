"""
NEXUS — Metrics Collection
==========================
Prometheus metrics for monitoring system performance and health.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Dict
import time

# Request metrics
REQUEST_COUNT = Counter(
    'nexus_requests_total',
    'Total number of requests processed',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'nexus_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

# External API metrics
EXTERNAL_API_CALLS = Counter(
    'nexus_external_api_calls_total',
    'Total number of external API calls',
    ['service', 'outcome']  # outcome: success or failure
)

# Circuit breaker metrics
CIRCUIT_BREAKER_STATE = Gauge(
    'nexus_circuit_breaker_state',
    'Circuit breaker state (0=closed, 1=open, 2=half_open)',
    ['service']
)

# Connection metrics
ACTIVE_WEBSOCKET_CONNECTIONS = Gauge(
    'nexus_websocket_connections_active',
    'Number of active WebSocket connections'
)

# Bulkhead metrics
BULKHEAD_ACTIVE = Gauge(
    'nexus_bulkhead_active',
    'Number of active executions in bulkhead',
    ['resource']
)

# Error metrics
ERROR_COUNT = Counter(
    'nexus_errors_total',
    'Total number of errors',
    ['type', 'component']
)


def record_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record request metrics."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)


def record_external_api_call(service: str, outcome: str):
    """Record external API call outcome."""
    EXTERNAL_API_CALLS.labels(service=service, outcome=outcome).inc()


def record_circuit_breaker_state(service: str, state: int):
    """Record circuit breaker state."""
    CIRCUIT_BREAKER_STATE.labels(service=service).set(state)


def set_active_websocket_connections(count: int):
    """Set active WebSocket connections gauge."""
    ACTIVE_WEBSOCKET_CONNECTIONS.set(count)


def set_bulkhead_active(resource: str, count: int):
    """Set bulkhead active executions gauge."""
    BULKHEAD_ACTIVE.labels(resource=resource).set(count)


def record_error(error_type: str, component: str):
    """Record an error occurrence."""
    ERROR_COUNT.labels(type=error_type, component=component).inc()


def get_metrics() -> tuple[str, str]:
    """Get metrics in Prometheus format."""
    return generate_latest(), CONTENT_TYPE_LATEST