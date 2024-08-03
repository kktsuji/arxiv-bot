"""Notify to webhooks of new papers on arXiv."""

from datetime import datetime, timezone, timedelta
import json
import os

import arxiv
import requests


def _make_query(keywords, categories, day):
    # https://info.arxiv.org/help/api/user-manual.html for query syntax
    query = "%28"
    for k in keywords:
        query += f'ti:"{k}" OR abs:"{k}" OR '
    query = query[:-4] + "%29 AND %28"
    for c in categories:
        query += f'cat:"{c}" OR '
    query = query[:-4] + "%29"
    query = f"{query} AND submittedDate:[{day} TO {day}235959]"
    return query


def _get_arxiv_results(query):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        max_results=100,
    )
    results = list(client.results(search))
    return results


def _make_post_contents(r):
    text = (
        f"Title: {r.title}\n"
        + f"First Author: {r.authors[0]}\n"
        + f"Published: {r.published}\n"
        + f"Entry: {r.pdf_url.replace('pdf','abs')[:-2]}\n"
        + f"PDF: {r.pdf_url}\n"
        + f"Categories: {r.categories}\n"
        + f"Abstract: {r.summary.replace('\n',' ')}\n"
    )
    return text


def _requests_post(webhook_url, text):
    tmp = "--------------\n"
    requests.post(
        webhook_url,
        data=json.dumps(
            {
                "text": text + tmp,
            }
        ),
        timeout=5.0,
    )


def _exec(params):
    webhook_url = params["webhook_url"]
    keywords = params["keywords"].split(",")
    categories = params["categories"].split(",")

    day = datetime.now(timezone.utc).date() - timedelta(days=1)
    day_m = day.strftime("%b")
    query = _make_query(keywords, categories, day.strftime("%Y%m%d"))
    results = _get_arxiv_results(query)
    num_results = len(results)

    text = f"New papers on {day_m} {day.day}, {day.year}.\n"
    text += f'Query: "{query}"\n'

    if num_results == 0:
        text += "No papers found.\n"
        _requests_post(webhook_url, text)
    else:
        text += f"{num_results} papers found.\n"
        _requests_post(webhook_url, text)
        for r in results:
            text = _make_post_contents(r)
            _requests_post(webhook_url, text)


def lambda_handler(event, context):
    """Lambda handler for AWS Lambda."""
    _exec(event)
    return {"statusCode": 200, "body": json.dumps("Process completed.")}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")
    params = {
        "webhook_url": os.getenv("WEBHOOK_URL"),
        "keywords": os.getenv("KEYWORDS"),
        "categories": os.getenv("CATEGORIES"),
    }
    _exec(params)
