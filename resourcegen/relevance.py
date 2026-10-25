"""후보 영상 관련도 점수: 대본 단어와 영상 제목·설명의 단어 겹침 비율."""
from dataclasses import dataclass

from .footage_search import Video
from .utils.text_utils import tokenize


@dataclass
class Scored:
    video: Video
    score: float

    def to_row(self, rank: int) -> dict:
        d = self.video.to_dict()
        d.update(rank=rank, score=round(self.score, 3))
        return d


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def overlap_score(script_text: str, video: Video) -> float:
    s = set(tokenize(script_text))
    v = set(tokenize(f"{video.title} {video.description}"))
    return jaccard(s, v)


def score_all(script_text: str, videos: list[Video]) -> list[Scored]:
    return [Scored(v, overlap_score(script_text, v)) for v in videos]


def rank(items: list[Scored], top_n: int) -> list[Scored]:
    return sorted(items, key=lambda s: s.score, reverse=True)[:top_n]
