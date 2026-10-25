"""입력 검사."""
from .exceptions import ConfigError, ScriptError

MIN_SCRIPT_CHARS = 50
MAX_SCRIPT_CHARS = 20000


def check_script(text: str) -> str:
    text = (text or "").strip()
    if len(text) < MIN_SCRIPT_CHARS:
        raise ScriptError(f"대본이 너무 짧습니다 ({len(text)}자, 최소 {MIN_SCRIPT_CHARS}자).")
    if len(text) > MAX_SCRIPT_CHARS:
        raise ScriptError(f"대본이 너무 깁니다 ({len(text)}자, 최대 {MAX_SCRIPT_CHARS}자).")
    return text


def require(value, name: str):
    if not value:
        raise ConfigError(f"{name} 설정이 필요합니다 (.env 또는 config/settings.yaml).")
    return value


def check_keywords(items, min_n: int = 1) -> list[str]:
    out, seen = [], set()
    for k in items or []:
        k = str(k).strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            out.append(k)
    if len(out) < min_n:
        raise ValueError(f"키워드가 {min_n}개 미만입니다.")
    return out
