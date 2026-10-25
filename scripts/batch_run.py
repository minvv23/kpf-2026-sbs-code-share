"""폴더 안의 대본(.txt)을 차례로 처리한다.

python scripts/batch_run.py --dir ./scripts_in
"""
import argparse
from pathlib import Path

from resourcegen import pipeline, script_parser
from resourcegen.utils.logging_utils import get_logger

log = get_logger("batch")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default="./output/batch")
    ap.add_argument("--skip-images", action="store_true")
    args = ap.parse_args()

    files = sorted(Path(args.dir).glob("*.txt"))
    log.info("대본 %d건", len(files))
    for f in files:
        try:
            script = script_parser.load(f)
            res = pipeline.run(script, Path(args.out) / f.stem,
                               pipeline.Options(skip_images=args.skip_images))
            log.info("%s: %s", f.name, res.summary())
        except Exception as e:  # noqa: BLE001
            log.error("%s 실패: %s", f.name, e)


if __name__ == "__main__":
    main()
