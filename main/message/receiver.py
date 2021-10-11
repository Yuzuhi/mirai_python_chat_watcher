import asyncio
import json
from typing import Optional, Dict, AsyncIterable

import aiohttp

from exceptions.exc import AuthorizeException
from main.message import const
from main.message.base import MessageBase
from modles.constant import GroupMessageType
from modles.messages import GroupMessage, GroupSender, MessageChain
from utils.queue import Queue


class MessageReceiver(MessageBase):
    """通过http协议从mirai-api-http读取聊天信息，并且放入缓存区"""

    async def listen(self, queue: Queue, interval: float = 0.1):
        """监听"""
        session_key = ""
        while not session_key:
            try:
                session_key = await self.authorize()
            except AuthorizeException:
                await asyncio.sleep(5)

        while True:
            async for new_msg in self._get_last_msg(session_key):
                if new_msg["type"] == GroupMessageType:
                    sender = new_msg["sender"]

                    new_model = GroupMessage(
                        sender=GroupSender(
                            id=sender["id"],
                            memberName=sender["memberName"],
                            specialTitle=sender["specialTitle"],
                            permission=sender["permission"],
                            joinTimestamp=sender["joinTimestamp"],
                            lastSpeakTimestamp=sender["lastSpeakTimestamp"],
                            muteTimeRemaining=sender["muteTimeRemaining"]
                        ),
                        message_chain=MessageChain(messages=new_msg["messageChain"])
                    )

                    queue.append(new_model)

            await asyncio.sleep(interval)

    async def _get_last_msg(self, session_key: str, count: int = 10) -> AsyncIterable:
        """从mirai-api-http缓存区获取聊天记录"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + const.MIRAI_FETCH_LATEST_MESSAGE % (session_key, count),
                                   data=json.dumps(session_key)) as response:
                # 目前只存储群消息
                result = await response.json()

        if result["code"] != 0:
            return

        yield result["data"]
