"""Notify to webhooks of new papers on arXiv."""

from datetime import datetime, timezone, timedelta
import json
import os

import arxiv
from openai import OpenAI
import requests


def _make_query(keywords, categories, day):
    # https://info.arxiv.org/help/api/user-manual.html for arXiv query syntax
    query = "%28"
    for k in keywords:
        k_tmp = f"'{k}'" if k.find(" ") != -1 else k
        query += f'ti:"{k_tmp}" OR abs:"{k_tmp}" OR '
    query = query[:-4] + "%29 AND %28"
    for c in categories:
        query += f'cat:"{c}" OR '
    query = query[:-4] + "%29"
    query = f"{query} AND submittedDate:[{day} TO {day}235959]"
    return query


def _get_arxiv_response(query):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        max_results=100,
    )
    results = list(client.results(search))
    return results


def _make_header_contents(day, num_results, keywords):
    day_m = day.strftime("%b")
    num = "No" if num_results == 0 else num_results
    found = f"{num} papers found" if num != 1 else f"{num} paper found"
    text = f"{found} on {day_m} {day.day}, {day.year} (keywords={keywords}).\n"

    return text


def _requests_post(webhook_url, text):
    requests.post(
        webhook_url,
        data=json.dumps({"text": text}),
        timeout=5.0,
    )


def _exec(params):
    webhook_url = params["webhook_url"]
    keywords_raw = params["keywords"]
    keywords = keywords_raw.split(",")
    keywords = list(set(keywords))
    keywords = [k for k in keywords if k != ""]
    categories = params["categories"].replace(" ", "").split(",")

    day = datetime.now(timezone.utc).date() - timedelta(days=1)
    query = _make_query(keywords, categories, day.strftime("%Y%m%d"))
    results = _get_arxiv_response(query)
    num_results = len(results)

    contents = _make_header_contents(day, num_results, keywords_raw)

    for r in results:
        # Slack syntax
        contents += f"- <{r.entry_id}|{r.title}>, {r.authors[0]} et al.\n"
    _requests_post(webhook_url, contents)


def lambda_handler(event, context):
    """Lambda handler for AWS Lambda."""
    try:
        _exec(event)
        result = {"statusCode": 200, "body": json.dumps("Process completed.")}
    except Exception as e:
        result = str(e)

    return result


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")
    params = {
        "webhook_url": os.getenv("WEBHOOK_URL"),
        "keywords": os.getenv("KEYWORDS"),
        "categories": os.getenv("CATEGORIES"),
    }
    _exec(params)
