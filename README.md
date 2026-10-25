# kpf-2026-sbs-code-share

2026년 한국언론진흥재단 디지털 미디어 서비스 개발 지원 사업으로 개발한
**AI를 활용한 비디오머그 스크립트 자료화면 검색 및 모션그래픽 에셋(asset) 생성 자동화**(SBS)의 공개 소스코드입니다.

영상 대본에서 자료화면 검색어와 그림으로 표현할 키워드를 뽑고,
검색어로 후보 영상을 찾아 정리하며, 키워드별 에셋 이미지를 만들어 한 번에 내려받을 수 있게 묶는 흐름을 담고 있습니다.
다른 언론사가 자사 제작 환경에 맞춰 바꿔 쓸 수 있도록 기본형(reference implementation)으로 정리했습니다.

## 구성

```
resourcegen/
  config.py              설정 로더 (환경변수 > config/settings.yaml > 기본값)
  script_parser.py       대본 읽기·전처리 (.txt)
  keyword_extractor.py   영상 검색어 / 에셋 키워드 추출 (단어 빈도)
  footage_search.py      영상 검색 (YouTube Data API)
  footage_filter.py      중복 제거, 금지어 필터
  relevance.py           관련도 점수 (단어 겹침), 정렬
  asset_generator.py     키워드별 이미지 생성 (병렬, 재시도)
  exporter.py            결과 파일 저장, zip 묶기
  pipeline.py            전체 흐름
  run.py                 명령행 진입점
  sample_data.py         동작 확인용 가상 데이터
  utils/                 로깅, 예외, 텍스트, 날짜, 입출력, 입력 검사, 재시도
scripts/
  batch_run.py           폴더 안 대본 일괄 처리
  keyword_preview.py     검색어·키워드만 미리 보기
  inspect_zip.py         결과 zip 구성 출력
  check_config.py        필수 설정 확인
tests/                   단위 테스트 (pytest)
config/
  settings.example.yaml  설정 파일 예시
sample/
  sample_script.txt      예시 대본
web/
  index.html             웹 화면 기본 틀
docs/
  architecture.md        처리 흐름
  data_format.md         입력·출력 데이터 형식
```

## 설치

Python 3.11 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                                  # 값 채우기
cp config/settings.example.yaml config/settings.yaml  # 선택
```

## 환경 설정

| 변수 | 설명 |
|---|---|
| `OUTPUT_DIR` | 결과물 저장 폴더 |
| `IMAGE_API_KEY`, `IMAGE_MODEL` | 이미지 생성 API 키와 모델명 |
| `YOUTUBE_API_KEY` | YouTube Data API 키 |
| `SEARCH_MAX_RESULTS` | 검색어당 가져올 영상 수 |
| `TOP_N` | 최종 후보 영상 수 |

API 키, 서비스 주소, 프롬프트 세부 지침, 이미지 스타일 자료는 저장소에 포함하지 않았습니다.
`keyword_extractor.py`의 추출 방식과 `asset_generator.py`의 `PROMPT_TEMPLATE`을 각사 제작 기준에 맞게 바꿔 사용하세요.

## 실행

```bash
# 예시 대본, 검색·이미지 없이 흐름 확인
python -m resourcegen.run --sample --skip-search --skip-images

# 실제 대본
python -m resourcegen.run --script sample/sample_script.txt

# 보조 스크립트
python scripts/check_config.py
python scripts/keyword_preview.py sample/sample_script.txt
python scripts/batch_run.py --dir ./scripts_in --skip-images
python scripts/inspect_zip.py output/20260101/resources_20260101.zip
```

테스트:

```bash
pytest -q
```

## 웹 화면

`web/index.html`은 대본 입력(파일 불러오기), 이슈 지역·기준 날짜 선택, 결과 영역(검색어, 에셋 이미지, 자료화면 후보),
일괄 다운로드 버튼만 담은 기본 틀입니다. 각사 환경의 API와 연결해 사용합니다.

## 이용 시 유의사항

- 이 도구는 후보 제안과 초안 생성까지만 합니다. 실제 영상에 쓸 자료화면은 원본 출처와 이용 조건을 편집자가 확인해야 합니다.
- 생성 이미지도 사실관계와 맥락에 맞는지 사람이 검토한 뒤 사용하세요.

## 라이선스

MIT License. `LICENSE` 파일을 참고하세요.
