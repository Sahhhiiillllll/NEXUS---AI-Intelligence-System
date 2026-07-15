"""
N.A.X.U.S — Resilience Patterns
===============================
Circuit breaker, retry with exponential backoff, and bulkhead patterns
for protecting external service calls.
"""

import asyncio
import logging
import random
import time
from enum import Enum
from functools import wraps
from typing import Any, Callable, Type, TypeVar, Union

from logger import get_logger

log = get_logger("resilient")

# Type variables for generic decorators
T = TypeVar('T')
R = TypeVar('R')


class CircuitBreakerState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, short-circuiting calls
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker for protecting external service calls.

    Tracks failures and opens after reaching failure threshold.
    After recovery timeout, allows limited test calls (half-open).
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        expected_exception: Type[BaseException] = Exception,
        success_threshold: int = 3,
        name: str = "circuit_breaker"
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening
            recovery_timeout: Seconds to wait before half-open attempt
            expected_exception: Exception type that counts as failure
            success_threshold: Number of successes in half-open to close again
            name: Identifier for logging and metrics
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.success_threshold = success_threshold
        self.name = name

        self._state = CircuitBreakerState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0
        self._success_count = 0
        self._lock = asyncio.Lock()

        log.info(
            f"CircuitBreaker '{name}' initialized",
            extra={
                "event": "circuit_breaker_init",
                "failure_threshold": failure_threshold,
                "recovery_timeout": recovery_timeout
            }
        )

    @property
    def state(self) -> CircuitBreakerState:
        """Current circuit breaker state."""
        return self._state

    @property
    def failure_count(self) -> int:
        """Current failure count."""
        return self._failure_count

    async def __aenter__(self):
        """Enter async context - checks if call should be allowed."""
        await self._lock.acquire()
        try:
            if self._state == CircuitBreakerState.OPEN:
                # Check if recovery timeout has elapsed
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitBreakerState.HALF_OPEN
                    self._success_count = 0
                    log.info(
                        f"CircuitBreaker '{self.name}' transitioning to HALF_OPEN",
                        extra={"event": "circuit_breaker_half_open"}
                    )
                else:
                    # Still in open state, raise exception
                    raise CircuitBreakerOpenException(
                        f"CircuitBreaker '{self.name}' is OPEN"
                    )
            # If CLOSED or HALF_OPEN, allow the call
            return self
        finally:
            self._lock.release()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context - updates state based on outcome."""
        await self._lock.acquire()
        try:
            if exc_type is None:
                # Success
                await self._on_success()
            elif issubclass(exc_type, self.expected_exception):
                # Failure of expected type
                await self._on_failure()
            # For unexpected exceptions, don't count as failure (let them propagate)
        finally:
            self._lock.release()

    async def _on_success(self):
        """Handle successful call."""
        if self._state == CircuitBreakerState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.success_threshold:
                self._state = CircuitBreakerState.CLOSED
                self._failure_count = 0
                log.info(
                    f"CircuitBreaker '{self.name}' transitioning to CLOSED",
                    extra={"event": "circuit_breaker_closed"}
                )
        elif self._state == CircuitBreakerState.CLOSED:
            # Reset failure count on success in closed state
            self._failure_count = 0

    async def _on_failure(self):
        """Handle failed call."""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitBreakerState.CLOSED:
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitBreakerState.OPEN
                log.warning(
                    f"CircuitBreaker '{self.name}' transitioning to OPEN",
                    extra={
                        "event": "circuit_breaker_opened",
                        "failure_count": self._failure_count
                    }
                )
        elif self._state == CircuitBreakerState.HALF_OPEN:
            # Any failure in half-open goes back to open
            self._state = CircuitBreakerState.OPEN
            log.warning(
                f"CircuitBreaker '{self.name}' transitioning to OPEN from HALF_OPEN",
                extra={"event": "circuit_breaker_opened_half"}
            )

    def is_open(self) -> bool:
        """Check if circuit breaker is open."""
        return self._state == CircuitBreakerState.OPEN

    def is_closed(self) -> bool:
        """Check if circuit breaker is closed."""
        return self._state == CircuitBreakerState.CLOSED

    def is_half_open(self) -> bool:
        """Check if circuit breaker is half open."""
        return self._state == CircuitBreakerState.HALF_OPEN

    @property
    def async_decorator(self):
        """
        Decorator for async functions that applies circuit breaker pattern.

        Returns:
            Decorator function that can be applied to async methods
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                async with self:
                    return await func(*args, **kwargs)
            return wrapper
        return decorator


class CircuitBreakerOpenException(Exception):
    """Raised when circuit breaker is open and blocks a call."""
    pass


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    jitter_factor: float = 0.1,
    retry_exceptions: Union[Type[BaseException], tuple[Type[BaseException], ...]] = Exception,
    name: str = "retry"
):
    """
    Decorator for async functions that adds exponential backoff with jitter.

    Args:
        max_attempts: Maximum number of attempts (including first try)
        base_delay: Base delay in seconds for exponential backoff
        max_delay: Maximum delay in seconds
        jitter_factor: Fraction of base_delay to add as jitter (0.0-1.0)
        retry_exceptions: Exception types that trigger retry
        name: Identifier for logging
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except retry_exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        # Last attempt failed
                        log.error(
                            f"Retry '{name}' exhausted after {max_attempts} attempts",
                            extra={
                                "event": "retry_exhausted",
                                "attempts": max_attempts,
                                "exception": str(e)
                            }
                        )
                        raise

                    # Calculate delay with exponential backoff and jitter
                    delay = min(
                        base_delay * (2 ** attempt) +
                        random.uniform(0, jitter_factor * base_delay),
                        max_delay
                    )

                    log.warning(
                        f"Retry '{name}' attempt {attempt + 1} failed, retrying in {delay:.2f}s",
                        extra={
                            "event": "retry_attempt",
                            "attempt": attempt + 1,
                            "max_attempts": max_attempts,
                            "delay": delay,
                            "exception": str(e)
                        }
                    )

                    await asyncio.sleep(delay)
                except Exception as e:
                    # Non-retryable exception, propagate immediately
                    log.error(
                        f"Retry '{name}' encountered non-retryable exception",
                        extra={
                            "event": "retry_non_retryable",
                            "exception": str(e)
                        }
                    )
                    raise

            # Should not reach here, but just in case
            raise last_exception

        return wrapper
    return decorator


class Bulkhead:
    """
    Bulkhead pattern for limiting concurrent resource consumption.

    Uses semaphore to limit number of concurrent executions.
    """

    def __init__(self, max_concurrent: int, name: str = "bulkhead"):
        """
        Initialize bulkhead.

        Args:
            max_concurrent: Maximum number of concurrent executions
            name: Identifier for logging
        """
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._max_concurrent = max_concurrent
        self._name = name
        self._active_count = 0
        self._lock = asyncio.Lock()

        log.info(
            f"Bulkhead '{name}' initialized with max_concurrent={max_concurrent}",
            extra={"event": "bulkhead_init", "max_concurrent": max_concurrent}
        )

    async def __aenter__(self):
        """Enter bulkhead - acquire semaphore slot."""
        await self._semaphore.acquire()
        async with self._lock:
            self._active_count += 1
            if self._active_count == self._max_concurrent:
                log.warning(
                    f"Bulkhead '{self._name}' at maximum capacity",
                    extra={
                        "event": "bulkhead_at_capacity",
                        "active_count": self._active_count,
                        "max_concurrent": self._max_concurrent
                    }
                )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit bulkhead - release semaphore slot."""
        async with self._lock:
            self._active_count -= 1
        self._semaphore.release()

    @property
    def active_count(self) -> int:
        """Current number of active executions."""
        return self._active_count

    @property
    def available_count(self) -> int:
        """Number of available executions slots."""
        return self._max_concurrent - self._active_count


def bulkhead(max_concurrent: int, name: str = "bulkhead"):
    """
    Decorator for async functions that applies bulkhead pattern.

    Args:
        max_concurrent: Maximum number of concurrent executions
        name: Identifier for logging
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        bulkhead_instance = Bulkhead(max_concurrent, name)

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            async with bulkhead_instance:
                return await func(*args, **kwargs)

        return wrapper
    return decorator