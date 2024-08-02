"""Notify to Slack"""

import datetime
import json
import os

import arxiv
import requests
from dotenv import load_dotenv  # delete for aws lambda
load_dotenv(".env")             # delete for aws lambda


def make_query(keywords, yesterday_str):
    query = "%28"
    for k in keywords:
        query += f'ti:"{k}" OR abs:"{k}" OR '
    query = query[:-4] + "%29"
    query = f"{query} AND submittedDate:[{yesterday_str} TO {yesterday_str}235959]"
    return query


def requests_post(webhook_url, text):
    requests.post(
        webhook_url,
        data=json.dumps(
            {
                "text": text,
            }
        ),
        timeout=5.0,
    )


def main():
    webhook_url = os.getenv("WEBHOOK_URL")
    keywords = os.getenv("KEYWORDS").split(",")

    today = datetime.datetime.now(datetime.timezone.utc).date()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_str = yesterday.strftime("%Y%m%d")
    yesterday_month_str = yesterday.strftime("%b")

    query = make_query(keywords, yesterday_str)

    client = arxiv.Client()

    search = arxiv.Search(
        # https://info.arxiv.org/help/api/user-manual.html for query syntax
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        max_results=100,
    )
    results = list(client.results(search))

    text = f"New papers on {yesterday_month_str} {yesterday.day}, {yesterday.year}.\n"
    text += f'"Query: {query}\n"'

    if len(results) == 0:
        text += "No papers found.\n"
        requests_post(webhook_url, text)
    else:
        text += f"{len(results)} papers found.\n"
        for r in results:
            text += "--------------\n" \
                + f"Title: {r.title}\n" \
                + f"First Author: {r.authors[0]}\n" \
                + f"Published: {r.published}\n" \
                + f"Entry: {r.pdf_url.replace("pdf","abs")[:-2]}\n" \
                + f"PDF: {r.pdf_url}\n" \
                + f"Categories: {r.categories}\n" \
                + f"Abstract: {r.summary.replace("\n"," ")}\n"
            requests_post(webhook_url, text)
            text = ""


if __name__ == "__main__":
    main()
