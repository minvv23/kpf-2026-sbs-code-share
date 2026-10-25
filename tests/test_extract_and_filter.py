from resourcegen import footage_filter, keyword_extractor, relevance


def test_frequency_extract(sample_script):
    ext = keyword_extractor.extract(sample_script)
    assert ext.video_queries and ext.asset_keywords


def test_dedupe(videos):
    assert len(footage_filter.dedupe(videos + videos)) == len(videos)


def test_banned_words(videos):
    kept = footage_filter.by_title_words(videos, ["tips"])
    assert all("tips" not in v.title.lower() for v in kept)


def test_rank(sample_script, videos):
    ranked = relevance.rank(relevance.score_all(sample_script.text, videos), 5)
    assert len(ranked) == 5
    assert ranked[0].score >= ranked[-1].score
