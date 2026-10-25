from datetime import date

from resourcegen import exporter, relevance
from resourcegen.utils import date_utils


def test_parse_date():
    assert date_utils.parse_date("20260101") == date(2026, 1, 1)


def test_zip(tmp_path, sample_script, videos):
    items = relevance.score_all(sample_script.text, videos[:3])
    files = exporter.save_outputs(tmp_path, sample_script.text, ["q1"], items)
    z = exporter.make_zip(tmp_path, [], files, name="t.zip")
    names = [n for n, _ in exporter.list_zip(z)]
    assert "footage_candidates.csv" in names
