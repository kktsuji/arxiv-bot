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


def _make_header_contents(day, day_m, query, num_results):
    num = "No" if num_results == 0 else num_results
    found = f"{num} papers found.\n\n" if num != 1 else f"{num} paper found.\n\n"
    text = (
        f"New papers on {day_m} {day.day}, {day.year}.\n\n"
        + found
        + "--------------\n\n"
        f'arXiv query: "{query}"\n\n'
        "About arXiv query syntax: https://info.arxiv.org/help/api/user-manual.html\n\n"
        "About this bot: https://github.com/kktsuji/arxiv-bot\n\n"
    )

    return text


def _make_main_contents(r, abstract):
    text = (
        f"Title: {r.title}\n\n"
        f"Authors: {r.authors[0]} et al.\n\n"
        f"Published: {r.published}\n\n"
        f"Link: {r.entry_id}\n\n"
        f"Categories: {r.categories}\n\n" + abstract
    )
    return text


def _get_openai_response(title, abstract):
    system_message = (
        "Generate a brief and simple summary of the document "
        "according to these formats:\n"
        "* Introduction:\n"
        "* Challenges:\n"
        "* Methods:\n"
        "* Novelties:\n"
        "* Results:\n"
        "* Performances:\n"
        "* Limitations:\n"
        "* Discussion:\n"
    )
    user_message = f"Title: {title}\nAbstract: {abstract}"

    # https://platform.openai.com/docs/overview for OpenAI API
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def _requests_post(webhook_url, text):
    tmp = "--------------\n\n"
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
    keywords = list(set(keywords))
    keywords = [k for k in keywords if k != ""]
    categories = params["categories"].replace(" ", "").split(",")

    day = datetime.now(timezone.utc).date() - timedelta(days=1)
    day_m = day.strftime("%b")
    query = _make_query(keywords, categories, day.strftime("%Y%m%d"))
    results = _get_arxiv_response(query)
    num_results = len(results)

    contents = _make_header_contents(day, day_m, query, num_results)
    _requests_post(webhook_url, contents)

    for r in results:
        abstract = r.summary.replace("\n", " ")
        if params["openai_api_key"] != "":
            abstract = _get_openai_response(r.title, abstract) + "\n\n"
        else:
            abstract = f"Abstract: {abstract}\n\n"
        contents = _make_main_contents(r, abstract)
        _requests_post(webhook_url, contents)


def lambda_handler(event, context):
    """Lambda handler for AWS Lambda."""
    os.environ["OPENAI_API_KEY"] = event["openai_api_key"]
    _exec(event)
    return {"statusCode": 200, "body": json.dumps("Process completed.")}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")
    params = {
        "webhook_url": os.getenv("WEBHOOK_URL"),
        "keywords": os.getenv("KEYWORDS"),
        "categories": os.getenv("CATEGORIES"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
    }
    _exec(params)
