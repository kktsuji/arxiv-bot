"""Unit tests for the main module."""

from arxiv_bot import _make_query


def test_make_query():
    """Unit test for _make_query."""
    keywords = ["dl", "deep learning"]
    categories = ["cs.AI", "cs.CV"]
    date = "20240101"
    expect = (
        '%28ti:"dl" OR abs:"dl" OR '
        "ti:\"'deep learning'\" OR abs:\"'deep learning'\"%29 AND "
        '%28cat:"cs.AI" OR cat:"cs.CV"%29 AND '
        "submittedDate:[20240101 TO 20240101235959]"
    )
    result = _make_query(keywords, categories, date)
    assert expect == result
