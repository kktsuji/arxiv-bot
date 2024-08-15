# arxiv-bot

Notify to webhooks of new papers on arXiv.

Generate a brief and short summary of papers by using OpenAI's ChatGPT.

## Webhook Settings

Get webhook url of the service you want to notify.

* [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
* [Microsoft Teams Webhooks](https://learn.microsoft.com/en-us/power-automate/teams/create-flows-power-apps-app)
* [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
* etc.

## (Optional) OpenAI Settings

Get OpenAI API Key if you want to summary papers.

Note: The OpenAI API is chargeable.

* [OpenAI API](https://openai.com/api/)

## Local Execution

### Check Environment

Check your environment. Ubuntu 22.04.4 LTS is only supported.

```bash
lsb_release -a
# Ubuntu 22.04.4 LTS
```

Clone this project.

```bash
git clone git@github.com:kktsuji/arxiv-bot.git
cd arxiv-bot
```

Python version must be 3.12.3.

```python
python --version
# Python 3.12.3
```

Install python packages.

```python
pip install -U pip
pip install -r requirements.txt
```

Configure environment variables.

```bash
vim .env

WEBHOOK_URL=https://YOUR_WEBHOOK_URL
KEYWORDS=keyword1,keyword2,keyword3
CATEGORIES=cs.AI,cs.CV,cs.LG,eess.IV
OPENAI_API_KEY=YOUR_API_KEY
```

| Key | Description |
|----------|----------|
| WEBHOOK_URL | The webhook url such as Slack, Teams, and other service APIs. |
| KEYWORDS | Keywords used in queries for arXiv searches.<br>Each keyword is separated by a comma with no spaces.<br>Keywords are used to search titles and abstracts and are searched for with "or".<br>For example, if the value "keyword1,key word2" is specified, paper containing keyword1 and papers containing 'key word2' will be displayed as search results (if a keyword contains spaces, single quotation marks are be used). |
| CATEGORIES | Categories used in queries for arXiv searches.<br>This follows the same rule of keywords (separated by comma without space, searched with "or"). And spaces are removed.<br>For more details, see [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy). |
| OPENAI_API_KEY | (Optional) OpenAI API Key.<br>If you do not use the paper summarization function, please leave blank in ``.env`` file like bellow:<br>OPENAI_API_KEY= |

Execute script.

```python
python arxiv_bot.py
```

(Optional) Execute unit tests.

```python
pytest
```

## AWS Execution

See [my blog post](https://tsuji.tech/arxiv-bot-aws/) for AWS Configuration to Automatically Notify Webhooks of New Papers.
