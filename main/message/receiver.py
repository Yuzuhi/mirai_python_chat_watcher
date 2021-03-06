import asyncio
import json
from collections import deque
from typing import Optional, Dict, AsyncIterable

import aiohttp

from exceptions.exc import AuthorizeException
from main.api.api import MIRAI_FETCH_LATEST_MESSAGE
from main.message.base import MessageBase
from modles.constant import GroupMessageType, FriendMessageType
from modles.messages import GroupMessage, GroupSender, MessageChain, PrivateMessage, FriendSender, GroupInfo


class MessageReceiver(MessageBase):
    """通过http协议从mirai-api-http读取聊天信息，并且放入缓存区"""

    async def listen(self, group_msg_buffer: deque, friend_msg_buffer: deque, interval: float = 0.1):
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
                            muteTimeRemaining=sender["muteTimeRemaining"],

                            group=GroupInfo(
                                id=sender["group"]["id"],
                                name=sender["group"]["name"],
                                permission=sender["group"]["permission"]

                            )
                        ),
                        message_chain=new_msg["messageChain"]
                    )

                    group_msg_buffer.append(new_model)

                elif new_msg["type"] == FriendMessageType:
                    sender = new_msg["sender"]

                    new_model = PrivateMessage(
                        sender=FriendSender(
                            id=sender["id"],
                            nickname=sender["nickname"],
                            remark=sender["remark"]
                        ),
                        message_chain=new_msg["messageChain"]
                    )

                    friend_msg_buffer.append(new_model)

            await asyncio.sleep(interval)

    async def _get_last_msg(self, session_key: str, count: int = 10) -> AsyncIterable:
        """从mirai-api-http缓存区获取聊天记录"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + MIRAI_FETCH_LATEST_MESSAGE % (session_key, count),
                                   data=json.dumps(session_key)) as response:
                # 目前只存储群消息
                result = await response.json()

        if result["code"] != 0:
            return

        yield result["data"]
