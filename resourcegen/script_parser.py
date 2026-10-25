"""대본 읽기와 전처리."""
from dataclasses import dataclass, field
from pathlib import Path

from .utils.io_utils import read_text
from .utils.text_utils import normalize, split_paragraphs, split_sentences, strip_brackets
from .utils.validators import check_script


@dataclass
class Script:
    text: str
    paragraphs: list[str] = field(default_factory=list)
    sentences: list[str] = field(default_factory=list)
    source: str = "input"

    @property
    def n_chars(self) -> int:
        return len(self.text)

    def summary(self) -> dict:
        return {
            "source": self.source,
            "chars": self.n_chars,
            "paragraphs": len(self.paragraphs),
            "sentences": len(self.sentences),
        }


def prepare(text: str, source: str = "input", drop_brackets: bool = False) -> Script:
    """공백을 정리하고 문단·문장으로 나눈다."""
    text = normalize(text)
    if drop_brackets:
        text = normalize(strip_brackets(text))
    text = check_script(text)
    return Script(text=text, paragraphs=split_paragraphs(text), sentences=split_sentences(text), source=source)


def load(path, drop_brackets: bool = False) -> Script:
    """텍스트 파일(.txt)에서 대본을 읽는다."""
    p = Path(path)
    if p.suffix.lower() not in (".txt", ".md"):
        raise ValueError(f"지원하지 않는 형식입니다: {p.suffix}")
    return prepare(read_text(p), source=p.name, drop_brackets=drop_brackets)


def chunk(script: Script, max_chars: int = 3000) -> list[str]:
    """긴 대본을 문단 경계에서 나눈다."""
    out, buf = [], ""
    for para in script.paragraphs:
        if buf and len(buf) + len(para) + 2 > max_chars:
            out.append(buf)
            buf = para
        else:
            buf = f"{buf}\n\n{para}" if buf else para
    if buf:
        out.append(buf)
    return out
