"""Unit tests for the main module."""

import datetime

import arxiv
import pytest

from arxiv_bot import _make_query, _get_arxiv_response


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


def test_get_arxiv_response(_get_expected_arxiv_response):
    """Unit test for _get_arxiv_response."""
    query = "id:1812.04948"
    expect = _get_expected_arxiv_response
    result = _get_arxiv_response(query)
    assert expect == result


@pytest.fixture
def _get_expected_arxiv_response():
    return [
        arxiv.Result(
            entry_id="http://arxiv.org/abs/1812.04948v3",
            updated=datetime.datetime(
                2019, 3, 29, 11, 8, 46, tzinfo=datetime.timezone.utc
            ),
            published=datetime.datetime(
                2018, 12, 12, 13, 59, 43, tzinfo=datetime.timezone.utc
            ),
            title="A Style-Based Generator Architecture for Generative Adversarial Networks",
            authors=[
                arxiv.Result.Author("Tero Karras"),
                arxiv.Result.Author("Samuli Laine"),
                arxiv.Result.Author("Timo Aila"),
            ],
            summary="We propose an alternative generator architecture for generative adversarial\nnetworks, borrowing from style transfer literature. The new architecture leads\nto an automatically learned, unsupervised separation of high-level attributes\n(e.g., pose and identity when trained on human faces) and stochastic variation\nin the generated images (e.g., freckles, hair), and it enables intuitive,\nscale-specific control of the synthesis. The new generator improves the\nstate-of-the-art in terms of traditional distribution quality metrics, leads to\ndemonstrably better interpolation properties, and also better disentangles the\nlatent factors of variation. To quantify interpolation quality and\ndisentanglement, we propose two new, automated methods that are applicable to\nany generator architecture. Finally, we introduce a new, highly varied and\nhigh-quality dataset of human faces.",
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
