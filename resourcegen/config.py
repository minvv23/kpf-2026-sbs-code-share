"""설정 로더.

우선순위: 환경변수 > config/settings.yaml > 기본값.
기본값은 동작 확인용이며, 실제 운영 값은 각사 환경에 맞게 정한다.
"""
import json
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv가 없으면 환경변수만 사용
    pass

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = Path(os.getenv("SETTINGS_PATH", ROOT / "config" / "settings.yaml"))


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_FILE = _load_yaml(SETTINGS_PATH)


def get(name: str, default=None, cast=str):
    """환경변수, 설정 파일, 기본값 순서로 값을 찾는다."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        raw = _FILE.get(name.lower(), default)
    if raw is None:
        return None
    if cast is bool:
        return str(raw).lower() in ("1", "true", "yes", "y")
    if cast in (dict, list):
        return raw if isinstance(raw, cast) else json.loads(raw)
    return cast(raw)


# 경로
OUTPUT_DIR = Path(get("OUTPUT_DIR", "./output"))
LOG_LEVEL = get("LOG_LEVEL", "INFO")

# 이미지 생성
IMAGE_API_KEY = get("IMAGE_API_KEY", "")
IMAGE_MODEL = get("IMAGE_MODEL", "")
IMAGE_SIZE = get("IMAGE_SIZE", "1024x1024")
IMAGE_WORKERS = get("IMAGE_WORKERS", 2, int)

# 영상 검색
YOUTUBE_API_KEY = get("YOUTUBE_API_KEY", "")
SEARCH_MAX_RESULTS = get("SEARCH_MAX_RESULTS", 10, int)
TOP_N = get("TOP_N", 10, int)

# 추출 개수
N_QUERIES = get("N_QUERIES", 3, int)
N_KEYWORDS = get("N_KEYWORDS", 5, int)

# 재시도
RETRY_MAX = get("RETRY_MAX", 2, int)
RETRY_WAIT_SEC = get("RETRY_WAIT_SEC", 2.0, float)


def summary() -> dict:
    """키 값은 빼고 현재 설정을 돌려준다 (로그용)."""
    return {
        "output_dir": str(OUTPUT_DIR),
        "image_model": IMAGE_MODEL or "(미설정)",
        "image_size": IMAGE_SIZE,
        "search_max_results": SEARCH_MAX_RESULTS,
        "top_n": TOP_N,
        "n_queries": N_QUERIES,
        "n_keywords": N_KEYWORDS,
    }
