"""영상 검색 (YouTube Data API v3). API 키는 환경변수로만 받는다."""
from dataclasses import asdict, dataclass

from . import config
from .utils.logging_utils import get_logger
from .utils.validators import require

log = get_logger(__name__)


@dataclass
class Video:
    video_id: str
    title: str
    channel: str
    published_at: str
    description: str = ""
    query: str = ""

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["url"] = self.url
        return d


def search(query: str, max_results: int | None = None) -> list[Video]:
    """검색어 하나로 영상 목록을 가져온다."""
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", developerKey=require(config.YOUTUBE_API_KEY, "YOUTUBE_API_KEY"), cache_discovery=False)
    data = yt.search().list(q=query, part="snippet", type="video",
                            maxResults=max_results or config.SEARCH_MAX_RESULTS).execute()
    out = []
    for item in data.get("items", []):
        sn = item.get("snippet", {})
        out.append(Video(video_id=item["id"]["videoId"], title=sn.get("title", ""), channel=sn.get("channelTitle", ""),
                         published_at=sn.get("publishedAt", ""), description=sn.get("description", ""), query=query))
    log.info("검색 '%s': %d건", query, len(out))
    return out


def search_many(queries: list[str]) -> list[Video]:
    pool = []
    for q in queries:
        pool.extend(search(q))
    return pool
