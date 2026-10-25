"""단순 재시도 데코레이터."""
import functools
import time

from .logging_utils import get_logger

log = get_logger(__name__)


def retry(times: int = 2, wait: float = 1.0, exceptions=(Exception,)):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:  # noqa: PERF203
                    last = e
                    if attempt < times:
                        log.warning("%s 실패 (%d/%d): %s", fn.__name__, attempt + 1, times, e)
                        time.sleep(wait * (attempt + 1))
            raise last
        return wrapper
    return deco
