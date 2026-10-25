"""대본에서 영상 검색어와 에셋 키워드를 뽑는다 (단어 빈도 기반)."""
from collections import Counter
from dataclasses import asdict, dataclass

from . import config
from .script_parser import Script
from .utils.text_utils import tokenize


@dataclass
class Extraction:
    video_queries: list[str]
    asset_keywords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def top_words(text: str, n: int) -> list[str]:
    return [w for w, _ in Counter(tokenize(text)).most_common(n)]


def extract(script: Script, n_queries: int | None = None, n_keywords: int | None = None) -> Extraction:
    """많이 나온 단어 순으로 검색어(두 단어씩)와 키워드를 만든다."""
    n_q = n_queries or config.N_QUERIES
    n_k = n_keywords or config.N_KEYWORDS
    words = top_words(script.text, n_q * 2 + n_k)
    queries = [" ".join(words[i:i + 2]) for i in range(0, min(len(words), n_q * 2), 2)]
    keywords = words[n_q * 2:] or words[:n_k]
    return Extraction(video_queries=queries or words[:1], asset_keywords=keywords[:n_k])
