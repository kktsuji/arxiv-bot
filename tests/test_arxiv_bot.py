"""Unit tests for the main module."""

import datetime

import arxiv

from arxiv_bot import (
    _make_query,
    _get_arxiv_response,
    _make_header_contents,
    _make_post_contents,
)


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


def test_get_arxiv_response():
    """Unit test for _get_arxiv_response."""
    query = "id:1812.04948"
    expect = _EXPECTED_ARXIV_RESPONSE
    result = _get_arxiv_response(query)
    assert expect == result


def test_make_header_contents_no_papers_found():
    """Unit test for _make_header_contents."""
    day = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    day_m = "Jan"
    query = "id:1812.04948"
    num_results = 0
    expect = (
        "New papers on Jan 1, 2024.\n\n"
        "No papers found.\n\n"
        "--------------\n\n"
        'arXiv query: "id:1812.04948"\n\n'
        "About arXiv query syntax: https://info.arxiv.org/help/api/user-manual.html\n\n"
        "About this bot: https://github.com/kktsuji/arxiv-bot\n\n"
    )
    result = _make_header_contents(day, day_m, query, num_results)
    assert expect == result


def test_make_header_contents_1_paper_found():
    """Unit test for _make_header_contents."""
    day = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    day_m = "Jan"
    query = "id:1812.04948"
    num_results = 1
    expect = (
        "New papers on Jan 1, 2024.\n\n"
        "1 paper found.\n\n"
        "--------------\n\n"
        'arXiv query: "id:1812.04948"\n\n'
        "About arXiv query syntax: https://info.arxiv.org/help/api/user-manual.html\n\n"
        "About this bot: https://github.com/kktsuji/arxiv-bot\n\n"
    )
    result = _make_header_contents(day, day_m, query, num_results)
    assert expect == result


def test_make_header_contents_2_papers_found():
    """Unit test for _make_header_contents."""
    day = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    day_m = "Jan"
    query = "id:1812.04948"
    num_results = 2
    expect = (
        "New papers on Jan 1, 2024.\n\n"
        "2 papers found.\n\n"
        "--------------\n\n"
        'arXiv query: "id:1812.04948"\n\n'
        "About arXiv query syntax: https://info.arxiv.org/help/api/user-manual.html\n\n"
        "About this bot: https://github.com/kktsuji/arxiv-bot\n\n"
    )
    result = _make_header_contents(day, day_m, query, num_results)
    assert expect == result


def test_make_post_contents():
    """Unit test for _make_post_contents."""
    r = _EXPECTED_ARXIV_RESPONSE[0]
    abstract = "This is an abstract.\n\n"
    expect = (
        "Title: A Style-Based Generator Architecture for Generative Adversarial Networks\n\n"
        "Authors: Tero Karras et al.\n\n"
        "Published: 2018-12-12 13:59:43+00:00\n\n"
        "Link: http://arxiv.org/abs/1812.04948v3\n\n"
        "Categories: ['cs.NE', 'cs.LG', 'stat.ML']\n\n"
        "This is an abstract.\n\n"
    )
    result = _make_post_contents(r, abstract)
    assert expect == result


_EXPECTED_ARXIV_RESPONSE = [
    arxiv.Result(
        entry_id="http://arxiv.org/abs/1812.04948v3",
        updated=datetime.datetime(2019, 3, 29, 11, 8, 46, tzinfo=datetime.timezone.utc),
        published=datetime.datetime(
            2018, 12, 12, 13, 59, 43, tzinfo=datetime.timezone.utc
        ),
        title="A Style-Based Generator Architecture for Generative Adversarial Networks",
        authors=[
            arxiv.Result.Author("Tero Karras"),
            arxiv.Result.Author("Samuli Laine"),
            arxiv.Result.Author("Timo Aila"),
        ],
        summary=(
            "We propose an alternative generator architecture "
            "for generative adversarial\nnetworks, borrowing "
            "from style transfer literature. "
            "The new architecture leads\nto an automatically learned, "
            "unsupervised separation of high-level attributes\n"
            "(e.g., pose and identity when trained on human faces) "
            "and stochastic variation\nin the generated images "
            "(e.g., freckles, hair), and it enables intuitive,"
            "\nscale-specific control of the synthesis. "
            "The new generator improves the\nstate-of-the-art "
            "in terms of traditional distribution quality metrics, "
            "leads to\ndemonstrably better interpolation properties, "
            "and also better disentangles the\nlatent factors of variation. "
            "To quantify interpolation quality and\ndisentanglement, "
            "we propose two new, automated methods that are applicable to\n"
            "any generator architecture. Finally, we introduce a new, highly "
            "varied and\nhigh-quality dataset of human faces."
        ),
        comment="CVPR 2019 final version",
        journal_ref=None,
        doi=None,
        primary_category="cs.NE",
        categories=["cs.NE", "cs.LG", "stat.ML"],
        links=[
            arxiv.Result.Link(
                "http://arxiv.org/abs/1812.04948v3",
                title=None,
                rel="alternate",
                content_type=None,
            ),
            arxiv.Result.Link(
                "http://arxiv.org/pdf/1812.04948v3",
                title="pdf",
                rel="related",
                content_type=None,
            ),
        ],
    )
]
