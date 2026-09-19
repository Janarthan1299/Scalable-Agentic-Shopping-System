"""Bounded exponential retry helper."""
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def with_retry(operation: Callable[[], T], max_retries: int = 2, base_delay: float = 0.01) -> T:
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except (TimeoutError, ConnectionError) as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(base_delay * (2 ** attempt))
    raise last_error or RuntimeError("Operation failed")
