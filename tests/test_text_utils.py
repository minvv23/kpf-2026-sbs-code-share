from resourcegen.utils import text_utils as t


def test_normalize_spaces():
    assert t.normalize("a  b\r\n\n\n\nc") == "a b\n\nc"


def test_split_paragraphs():
    assert t.split_paragraphs("가\n\n나\n\n\n다") == ["가", "나", "다"]


def test_tokenize_drops_stopwords():
    assert "그리고" not in t.tokenize("그리고 하천 수위")


def test_safe_filename():
    assert t.safe_filename('a/b:c*?') == "a_b_c"


def test_truncate():
    assert t.truncate("abcdef", 4) == "abc…"
