import json

import aiohttp

from main.message.base import MessageBase
from modles.events import SendGroupMessageEvent
from utils.queue import Queue


class MessageHandler(MessageBase):
    """从缓存区读取mirai bot的消息，并通过自定义的方法来处理并通过http协议发送给mirai-api-http"""

    async def listen(self, queue: Queue, interval: float = 0.5):
        pass

    async def _send_group_message(self, session_key, event: SendGroupMessageEvent):
        """发送群消息事件"""
        if not isinstance(event, SendGroupMessageEvent):
            return

        if event.func:
            event.message.text = event.func()

        message_chain = [event.message.json()]

        data = {
            "sessionKey": session_key,
            "target": event.target,
            "messageChain": message_chain
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(event.api, data=json.dumps(data)) as response:
                print('发送群消息')
