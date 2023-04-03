# WeChatHelper
Collect, analyze, and send messages on WeChat using Wechaty and GPT.

Features:

1. Host WeChat bot that can save all your text messages into csv.
2. Summarize group chats using GPT.

Usage:

1. You'll need to generate an uuid first and request a token from http://pad-local.com/#/tokens , modify all related values in start.sh and bot.py.

2. Start the Wechaty service
```shell
sh start.sh
```

3. Start the bot
```python
pythn bot.py
```

4. After collecting the messages, use parse_csv.py to get a merged version of a group chat history.

5. Use GPT to summarize the group chat history.