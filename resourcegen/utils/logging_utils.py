"""로깅 설정."""
import logging
import sys

_CONFIGURED = False


def setup_logging(level: str = "INFO") -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level.upper())
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)


class Timer:
    """with 블록 실행 시간을 로그로 남긴다."""

    def __init__(self, logger: logging.Logger, label: str):
        self.logger = logger
        self.label = label

    def __enter__(self):
        import time
        self._t = time.time()
        return self

    def __exit__(self, *exc):
        import time
        self.logger.info("%s: %.1f초", self.label, time.time() - self._t)
        return False
