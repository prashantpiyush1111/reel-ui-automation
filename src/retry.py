import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry(
    operation: Callable[[], T | None],
    attempts: int,
    delay_seconds: float,
) -> T | None:
    for attempt in range(max(1, attempts)):
        result = operation()
        if result is not None:
            return result
        if attempt + 1 < attempts:
            time.sleep(delay_seconds)
    return None
