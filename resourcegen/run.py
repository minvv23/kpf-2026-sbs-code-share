"""명령행 진입점.

python -m resourcegen.run --script sample/sample_script.txt
"""
import argparse
import json
import sys

from . import config, pipeline, script_parser
from .sample_data import SAMPLE_SCRIPT
from .utils.exceptions import ResourceGenError
from .utils.logging_utils import get_logger, setup_logging


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="대본 기반 자료화면 검색 및 에셋 이미지 생성")
    ap.add_argument("--script", help="대본 텍스트 파일 경로 (.txt)")
    ap.add_argument("--sample", action="store_true", help="내장 예시 대본 사용")
    ap.add_argument("--out", default=None, help="출력 폴더")
    ap.add_argument("--skip-search", action="store_true", help="영상 검색 생략")
    ap.add_argument("--skip-images", action="store_true", help="이미지 생성 생략")
    ap.add_argument("--top-n", type=int, default=config.TOP_N, help="후보 영상 개수")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    setup_logging(config.LOG_LEVEL)
    log = get_logger("resourcegen")
    log.info("설정: %s", config.summary())
    try:
        if args.sample or not args.script:
            script = script_parser.prepare(SAMPLE_SCRIPT, source="sample")
        else:
            script = script_parser.load(args.script)
        log.info("대본: %s", script.summary())
        opts = pipeline.Options(skip_search=args.skip_search, skip_images=args.skip_images, top_n=args.top_n)
        result = pipeline.run(script, args.out, opts)
    except ResourceGenError as e:
        log.error("%s", e)
        return 1
    print(json.dumps(result.summary(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
