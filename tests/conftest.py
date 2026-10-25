import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from resourcegen.sample_data import SAMPLE_SCRIPT, fake_videos  # noqa: E402


@pytest.fixture
def sample_script():
    from resourcegen import script_parser
    return script_parser.prepare(SAMPLE_SCRIPT, source="test")


@pytest.fixture
def videos():
    return fake_videos(12)
