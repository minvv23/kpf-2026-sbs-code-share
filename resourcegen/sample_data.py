"""동작 확인용 가상 데이터."""
import random

from .footage_search import Video

SAMPLE_SCRIPT = """오늘 오전 한 지역에 강한 비가 내리면서 하천 수위가 빠르게 올라갔습니다.
당국은 저지대 주민들에게 대피를 권고했고, 일부 도로는 통제됐습니다.

기상청은 내일까지 비가 이어질 것으로 내다봤습니다.
전문가들은 배수 시설 점검과 안전한 장소로의 이동을 당부했습니다.
"""

TITLES = [
    "Heavy rain causes river to rise", "Residents evacuate low-lying areas", "Roads closed after flooding",
    "Weather service warns of more rain", "How drainage systems work", "Flood safety tips",
    "City cleanup after storm", "Rainfall record this week",
]
CHANNELS = ["News Channel A", "News Channel B", "Public Broadcaster", "Local TV", "Weather Desk"]


def fake_videos(n: int = 12, seed: int = 0) -> list[Video]:
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        out.append(Video(video_id=f"sample{i:04d}", title=rnd.choice(TITLES), channel=rnd.choice(CHANNELS),
                         published_at="2026-01-01T00:00:00Z", description="sample description", query="sample"))
    return out
