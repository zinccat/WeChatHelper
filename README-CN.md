# 微信助手
使用 Wechaty 和 GPT 收集、分析和发送微信消息的用户友好工具。

## 功能
1. 托管一个微信机器人，将所有文本消息保存到 CSV 文件中。
2. 使用 GPT 对群聊历史进行总结。

## 使用方法

### 先决条件
0. 安装 Docker (https://docs.docker.com/engine/install/) 和 Wechaty (https://github.com/wechaty/python-wechaty)。
1. 生成 UUID (https://www.uuid.online/) 并从 http://pad-local.com/#/tokens 请求令牌。
2. 使用获得的令牌修改 `start.sh` 和 `bot.py` 中的相关值。

### 步骤

1. 启动 Wechaty 服务：

如果您使用的是 Linux/MacOS，
```shell
sh start.sh
```
如果您使用的是 Windows，请查看 https://wechaty.js.org/2021/05/18/win10-use-docker-build-web-protocol-server-develop-bot/。

2. 将`bot.py`中以下行改为自己昵称后启动机器人：
```python
if to_contact.payload.name != "please change to your own wechat alias":
```

```python
python bot.py
```

3. 在收集到消息后，使用 `summary.py` 生成一个合并版本的群聊历史并对其进行总结。确保设置要处理的文件。

```python
python summary.py
```

享受使用微信助手管理和分析您的微信消息！