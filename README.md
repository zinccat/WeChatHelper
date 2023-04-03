# WeChatHelper
A user-friendly tool to collect, analyze, and send messages on WeChat using Wechaty and GPT.

## Features
1. Host a WeChat bot that can save all your text messages into a CSV file.
2. Summarize group chat's history using GPT.

## Usage

### Prerequisites
1. Generate a UUID and request a token from http://pad-local.com/#/tokens.
2. Modify the related values in `start.sh` and `bot.py` with the obtained token.

### Steps

1. Start the Wechaty service:
```shell
sh start.sh
```

2. Launch the bot:
```python
python bot.py
```

3. After collecting the messages, use `summary.py` to generate a merged version of a group chat history and summarize it. Make sure to set the file you want to process.

```python
python summary.py
```

Enjoy using WeChatHelper to manage and analyze your WeChat messages!