"""대본에서 뽑힌 검색어·키워드만 미리 본다 (검색·생성 없음).

python scripts/keyword_preview.py sample/sample_script.txt
"""
import argparse
import json

from resourcegen import keyword_extractor, script_parser


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()
    script = script_parser.load(args.path)
    ext = keyword_extractor.extract(script)
    print(json.dumps(ext.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
