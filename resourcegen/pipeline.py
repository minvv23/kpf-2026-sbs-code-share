"""대본 하나를 처리하는 전체 흐름.

대본 전처리 → 검색어·키워드 추출 → 영상 검색·정리·점수 → 이미지 생성 → 저장·zip
"""
from dataclasses import dataclass, field
from pathlib import Path

from . import asset_generator, config, exporter, footage_filter, footage_search, keyword_extractor, relevance
from .script_parser import Script
from .utils.date_utils import yyyymmdd
from .utils.io_utils import write_json
from .utils.logging_utils import Timer, get_logger

log = get_logger(__name__)


@dataclass
class Options:
    skip_search: bool = False
    skip_images: bool = False
    top_n: int = field(default_factory=lambda: config.TOP_N)


@dataclass
class Result:
    extraction: keyword_extractor.Extraction
    footage: list = field(default_factory=list)
    assets: list = field(default_factory=list)
    filter_stats: dict = field(default_factory=dict)
    zip_path: Path | None = None

    def summary(self) -> dict:
        return {
            "queries": self.extraction.video_queries,
            "keywords": self.extraction.asset_keywords,
            "footage": len(self.footage),
            "assets_ok": sum(a.ok for a in self.assets),
            "assets_failed": sum(not a.ok for a in self.assets),
            "filter": self.filter_stats,
            "zip": str(self.zip_path) if self.zip_path else None,
        }


def run(script: Script, out_dir=None, opts: Options | None = None) -> Result:
    opts = opts or Options()
    out_dir = Path(out_dir or config.OUTPUT_DIR / yyyymmdd())

    with Timer(log, "대본 분석"):
        ext = keyword_extractor.extract(script)
    result = Result(extraction=ext)

    if not opts.skip_search:
        with Timer(log, "영상 검색"):
            pool = footage_search.search_many(ext.video_queries)
            kept, result.filter_stats = footage_filter.apply_all(pool)
            scored = relevance.score_all(script.text, kept)
            result.footage = relevance.rank(scored, opts.top_n)

    if not opts.skip_images:
        with Timer(log, "이미지 생성"):
            result.assets = asset_generator.generate_all(ext.asset_keywords, out_dir / "assets")

    files = exporter.save_outputs(out_dir, script.text, ext.video_queries, result.footage)
    result.zip_path = exporter.make_zip(out_dir, result.assets, files)
    write_json(out_dir / "summary.json", result.summary())
    log.info("완료: %s", result.zip_path)
    return result
