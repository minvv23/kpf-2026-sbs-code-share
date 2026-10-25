"""결과 zip 구성을 출력한다.

python scripts/inspect_zip.py output/20260101/resources_20260101.zip
"""
import sys

from resourcegen.exporter import list_zip


def main():
    if len(sys.argv) < 2:
        print("사용법: python scripts/inspect_zip.py <zip 경로>")
        return
    total = 0
    for name, size in list_zip(sys.argv[1]):
        print(f"{size:>10}  {name}")
        total += size
    print(f"{total:>10}  합계")


if __name__ == "__main__":
    main()
