import pytest

from resourcegen import script_parser
from resourcegen.utils.exceptions import ScriptError


def test_prepare(sample_script):
    assert sample_script.n_chars > 50
    assert len(sample_script.paragraphs) == 2


def test_too_short():
    with pytest.raises(ScriptError):
        script_parser.prepare("짧은 대본")


def test_chunk(sample_script):
    parts = script_parser.chunk(sample_script, max_chars=80)
    assert len(parts) >= 2
