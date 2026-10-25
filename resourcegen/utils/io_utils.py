"""파일 입출력."""
import csv
import json
from pathlib import Path


def ensure_dir(path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_text(path) -> str:
    """UTF-8로 읽고, 실패하면 CP949로 다시 읽는다."""
    raw = Path(path).read_bytes()
    for enc in ("utf-8-sig", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def write_text(path, text: str) -> Path:
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(text, encoding="utf-8")
    return p


def write_json(path, obj) -> Path:
    return write_text(path, json.dumps(obj, ensure_ascii=False, indent=2))


def read_json(path):
    return json.loads(read_text(path))


def write_csv(path, rows: list[dict], columns: list[str]) -> Path:
    """엑셀에서 한글이 깨지지 않게 BOM을 붙여 저장한다."""
    p = Path(path)
    ensure_dir(p.parent)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return p
