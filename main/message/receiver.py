import asyncio
import json
from typing import Optional, Dict

import aiohttp

from exceptions.exc import AuthorizeException
from main.message import const
from main.message.base import MessageBase
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
            new_msg = await self._get_last_msg(session_key)
            if new_msg:
                queue.append(new_msg)
            await asyncio.sleep(interval)

    async def _get_last_msg(self, session_key: str, count: int = 10) -> Optional[Dict]:
        """从mirai-api-http缓存区获取聊天记录"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + const.MIRAI_FETCH_LATEST_MESSAGE % (session_key, count),
                                   data=json.dumps(session_key)) as response:
                # 目前只存储群消息
                result = await response.json()

        if result["code"] != 0:
            return

        return result["data"]
