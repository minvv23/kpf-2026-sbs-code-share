"""검색 결과 정리: 중복 제거."""
from collections import Counter

from .footage_search import Video


def dedupe(videos: list[Video]) -> list[Video]:
    seen, out = set(), []
    for v in videos:
        if v.video_id not in seen:
            seen.add(v.video_id)
            out.append(v)
    return out


def by_title_words(videos: list[Video], banned: list[str]) -> list[Video]:
    banned = [b.lower() for b in banned if b]
    return [v for v in videos if not any(b in v.title.lower() for b in banned)]


def stats(before: list[Video], after: list[Video]) -> dict:
    return {
        "searched": len(before),
        "kept": len(after),
        "removed": len(before) - len(after),
        "by_query": dict(Counter(v.query for v in after)),
    }


def apply_all(videos: list[Video]) -> tuple[list[Video], dict]:
    kept = dedupe(videos)
    return kept, stats(videos, kept)
