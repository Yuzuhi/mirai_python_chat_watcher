import json

import aiohttp

from main.message.base import MessageBase
from utils.queue import Queue


class MessageHandler(MessageBase):
    """从缓存区读取mirai bot的消息，并通过自定义的方法来处理并通过http协议发送给mirai-api-http"""

    async def listen(self, queue: Queue, interval: float = 0.5):
        pass

    async def _send_group_message(self, session_key, event: SendGroupMessageEvent):
        """发送群消息事件"""
        if not isinstance(event,SendGroupMessageEvent):
            return

        data = {
            "sessionKey": session_key,
            "target": event.target,
            "messageChain": [
                {"type": "Plain", "text": event.message}
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(event.url, data=json.dumps(data)) as response:
                print('发送群消息')
