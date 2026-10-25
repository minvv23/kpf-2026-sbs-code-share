"""필수 설정이 채워졌는지 확인한다 (값은 출력하지 않음)."""
from resourcegen import config

REQUIRED = ["IMAGE_API_KEY", "IMAGE_MODEL", "YOUTUBE_API_KEY"]


def main():
    for name in REQUIRED:
        print(f"{name:<18} {'설정됨' if getattr(config, name) else '없음'}")
    for k, v in config.summary().items():
        print(f"{k:<18} {v}")


if __name__ == "__main__":
    main()
