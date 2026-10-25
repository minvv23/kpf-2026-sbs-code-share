"""패키지 공통 예외."""


class ResourceGenError(Exception):
    """기본 예외."""


class ConfigError(ResourceGenError):
    """필수 설정값이 없거나 잘못됨."""


class ScriptError(ResourceGenError):
    """입력 대본이 비었거나 너무 짧음."""


class SearchError(ResourceGenError):
    """영상 검색 API 호출 실패."""


class GenerationError(ResourceGenError):
    """이미지 생성 실패."""


class ExportError(ResourceGenError):
    """결과물 저장 실패."""
