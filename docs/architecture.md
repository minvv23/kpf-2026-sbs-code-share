# 처리 흐름

```
대본(.txt 또는 직접 입력)
   │
   ▼
script_parser      공백 정리, 문단·문장 분리, 길이 검사
   │
   ▼
keyword_extractor  단어 빈도로 영상 검색어 / 에셋 키워드 추출
   ├──────────────────────────────┐
   ▼                              ▼
footage_search     영상 검색       asset_generator   키워드별 이미지 생성
footage_filter     중복 정리       (병렬, 실패 시 재시도)
relevance          관련도 점수·정렬
   │                              │
   └──────────────┬───────────────┘
                  ▼
exporter          script.txt, search_queries.txt, footage_candidates.csv,
                  assets/*.png 를 zip 하나로 묶음
```

## 모듈별 역할

| 모듈 | 역할 |
|---|---|
| `config.py` | 환경변수와 설정 파일 읽기 |
| `script_parser.py` | 대본 읽기, 전처리, 긴 대본 나누기 |
| `keyword_extractor.py` | 검색어·키워드 추출 |
| `footage_search.py` | 영상 검색 API 호출 |
| `footage_filter.py` | 중복 제거, 금지어 필터, 통계 |
| `relevance.py` | 단어 겹침 점수, 정렬 |
| `asset_generator.py` | 이미지 생성 API 호출, 병렬 처리 |
| `exporter.py` | 결과 파일 저장, zip 묶기 |
| `pipeline.py` | 위 단계를 차례로 실행 |
| `run.py` | 명령행 진입점 |

## 사람의 역할

이 도구는 후보 제안과 초안 생성까지만 담당한다. 어떤 자료화면과 이미지를 실제 영상에 쓸지는
편집자가 원본 출처와 이용 조건을 확인한 뒤 정한다.
