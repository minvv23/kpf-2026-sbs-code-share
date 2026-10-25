"""텍스트 정리 함수."""
import re
import unicodedata

_WS = re.compile(r"[ \t 　]+")
_MULTI_NL = re.compile(r"\n{3,}")
_SENT_END = re.compile(r"(?<=[.!?。])\s+|(?<=다\.)\s*")
_BRACKET = re.compile(r"\([^)]*\)|\[[^\]]*\]")
_FILENAME_BAD = re.compile(r'[\\/:*?"<>|]+')

STOPWORDS = {
    "그리고", "그러나", "하지만", "그래서", "또한", "이번", "지난", "오늘", "현재", "관련",
    "통해", "대한", "위해", "있는", "있다", "했다", "한다", "것으로", "등", "및", "이", "그", "저",
}


def normalize(text: str) -> str:
    """유니코드 정규화, 공백 정리."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WS.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return _MULTI_NL.sub("\n\n", text).strip()


def strip_brackets(text: str) -> str:
    """괄호 안 내용(지문, 자막 지시 등)을 지운다."""
    return _BRACKET.sub("", text)


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in normalize(text).split("\n\n") if p.strip()]


def split_sentences(text: str) -> list[str]:
    out = []
    for para in split_paragraphs(text):
        out.extend(s.strip() for s in _SENT_END.split(para) if s and s.strip())
    return out


def tokenize(text: str) -> list[str]:
    """공백 기준 단순 토큰화 (형태소 분석 없음)."""
    tokens = re.findall(r"[0-9A-Za-z가-힣]+", text.lower())
    return [t for t in tokens if len(t) > 1 and t not in STOPWORDS]


def safe_filename(name: str, max_len: int = 60) -> str:
    name = _FILENAME_BAD.sub("_", name).strip(" ._")
    return (name or "untitled")[:max_len]


def truncate(text: str, n: int = 80) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"
