"""결과물 저장과 zip 묶기."""
import zipfile
from pathlib import Path

from .asset_generator import Asset
from .relevance import Scored
from .utils.date_utils import yyyymmdd
from .utils.io_utils import ensure_dir, write_csv, write_text

CSV_COLUMNS = ["rank", "title", "channel", "published_at", "url", "score"]


def footage_rows(items: list[Scored]) -> list[dict]:
    return [s.to_row(i) for i, s in enumerate(items, 1)]


def save_outputs(out_dir, script_text: str, queries: list[str], footage: list[Scored]) -> dict:
    out = ensure_dir(out_dir)
    return {
        "script": write_text(out / "script.txt", script_text),
        "queries": write_text(out / "search_queries.txt", "\n".join(queries)),
        "footage": write_csv(out / "footage_candidates.csv", footage_rows(footage), CSV_COLUMNS),
    }


def make_zip(out_dir, assets: list[Asset], files: dict, name: str | None = None) -> Path:
    out = ensure_dir(out_dir)
    zpath = out / (name or f"resources_{yyyymmdd()}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for a in assets:
            if a.ok:
                z.write(a.path, f"assets/{Path(a.path).name}")
        for p in files.values():
            z.write(p, Path(p).name)
    return zpath


def list_zip(path) -> list[tuple[str, int]]:
    with zipfile.ZipFile(path) as z:
        return [(i.filename, i.file_size) for i in z.infolist()]
