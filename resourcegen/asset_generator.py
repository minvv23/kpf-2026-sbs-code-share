"""에셋 이미지 생성.

키워드 하나당 이미지 한 장을 만든다. 프롬프트는 일반적인 예시이며,
스타일과 세부 지침은 각사 디자인 기준에 맞춰 바꿔 쓴다.
"""
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from . import config
from .utils.exceptions import GenerationError
from .utils.io_utils import ensure_dir
from .utils.logging_utils import get_logger
from .utils.retry import retry
from .utils.text_utils import safe_filename
from .utils.validators import require

log = get_logger(__name__)

PROMPT_TEMPLATE = "A simple illustration of {keyword} on a plain background."


@dataclass
class Asset:
    keyword: str
    path: Path | None = None
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.path is not None


def build_prompt(keyword: str, template: str | None = None) -> str:
    return (template or PROMPT_TEMPLATE).format(keyword=keyword)


def _client():
    from openai import OpenAI
    return OpenAI(api_key=require(config.IMAGE_API_KEY, "IMAGE_API_KEY"))


@retry(times=config.RETRY_MAX, wait=config.RETRY_WAIT_SEC)
def generate_one(keyword: str, out_dir: Path, template: str | None = None) -> Path:
    resp = _client().images.generate(model=require(config.IMAGE_MODEL, "IMAGE_MODEL"),
                                     prompt=build_prompt(keyword, template), size=config.IMAGE_SIZE, n=1)
    b64 = resp.data[0].b64_json
    if not b64:
        raise GenerationError(f"이미지 응답이 비었습니다: {keyword}")
    path = ensure_dir(out_dir) / f"{safe_filename(keyword)}.png"
    path.write_bytes(base64.b64decode(b64))
    return path


def generate_all(keywords: list[str], out_dir, template: str | None = None, workers: int | None = None) -> list[Asset]:
    out_dir = Path(out_dir)
    results = {k: Asset(k) for k in keywords}
    with ThreadPoolExecutor(max_workers=workers or config.IMAGE_WORKERS) as ex:
        futs = {ex.submit(generate_one, k, out_dir, template): k for k in keywords}
        for f in as_completed(futs):
            k = futs[f]
            try:
                results[k].path = f.result()
                log.info("생성 완료: %s", k)
            except Exception as e:  # noqa: BLE001
                results[k].error = str(e)
                log.warning("생성 실패: %s (%s)", k, e)
    return [results[k] for k in keywords]
