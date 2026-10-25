# 데이터 형식

## 1. 입력

- 대본: UTF-8(또는 CP949) 텍스트. 최소 50자, 최대 20,000자.

## 2. 추출 결과 (`keyword_extractor.Extraction`)

```json
{
  "video_queries": ["검색어 1", "검색어 2"],
  "asset_keywords": ["사물 1", "사물 2"]
}
```

## 3. 후보 영상 CSV (`footage_candidates.csv`)

| 열 | 설명 |
|---|---|
| rank | 순위 |
| title | 영상 제목 |
| channel | 채널명 |
| published_at | 게시 시각 (UTC) |
| url | 영상 주소 |
| score | 관련도 점수 (0~1) |

## 4. zip 구성

```
resources_YYYYMMDD.zip
  assets/<키워드>.png
  footage_candidates.csv
  script.txt
  search_queries.txt
```

## 5. 실행 요약 (`summary.json`)

```json
{
  "queries": [], "keywords": [],
  "footage": 0, "assets_ok": 0, "assets_failed": 0,
  "filter": {"searched": 0, "kept": 0, "removed": 0, "by_query": {}},
  "zip": "output/.../resources_YYYYMMDD.zip"
}
```
