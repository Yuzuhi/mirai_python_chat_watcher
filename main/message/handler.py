import asyncio
import json
import os
from collections import deque
from typing import Callable, Dict, Optional, Tuple, Any, Union, Iterable

import aiohttp

from main.api import url as URL

from main.api import api as mirai_api

from main.message.base import MessageBase
from modles.command import GroupCommand, PrivateCommand

from modles.constant import GroupMessageType
from modles.events import SendGroupMessageEvent, Message
from modles.messages import GroupMessage, PrivateMessage, SingleGroupMessage, SinglePrivateMessage
from utils.queue import Queue


class CommandHandler(MessageBase):
    """从缓存区读取mirai bot的消息，并通过自定义的方法来处理并通过http协议发送给mirai-api-http"""

    def __init__(self, url: str, port: int, auth_key: str, bot_qq: int):

        super().__init__(url, port, auth_key, bot_qq)

        # mirai_bot api http
        self.url = f"http://{url}:{port}"
        # 当前循环中的群消息
        self.group_message: Optional[SingleGroupMessage] = None
        # 当前循环中的好友消息
        self.private_message: Optional[SinglePrivateMessage] = None

    async def listen(
            self,
            group_msg_buffer: deque,
            friend_msg_buffer: deque,
            group_chat_commands: Dict[int, Dict[str, GroupCommand]],
            private_chat_commands: Dict[str, PrivateCommand],
            interval: float = 0.5
    ):

        """

        :param group_msg_buffer: 保存群聊消息的列表
        :param friend_msg_buffer: 保存好友消息的列表
        :param group_chat_commands: 保存群聊消息命令的字典
        :param private_chat_commands: 保存个人消息命令的字典
        :param interval: 每次循环休息时间
        :return:
        """

        while True:
            group_msg: Optional[GroupMessage] = group_msg_buffer.pop()
            private_msg: Optional[PrivateMessage] = friend_msg_buffer.pop()

            if not group_msg and not private_msg:
                await asyncio.sleep(0.1)
                continue

            self.private_message = SinglePrivateMessage(
                sender=private_msg.sender,
                message=dict()
            )

            self.group_message = SingleGroupMessage(
                sender=group_msg.sender,
                message=dict()
            )

            if group_msg:

                if group_chat_commands.get(group_msg.sender.id):
                    # 发现有匹配当前群的命令
                    for single_msg in group_msg.message_chain:
                        for command, event in group_chat_commands[group_msg.sender.id].items():
                            if not single_msg["text"].startswith(command):
                                continue

                            self.group_message.message = single_msg
                            # 执行命令
                            await self._distribute(event.api, group_msg.sender.group.id, event.func, event.params)

                            break
                        else:
                            continue

                        break

            if private_msg:

                for single_msg in private_msg.message_chain:
                    for command, event in private_chat_commands.items():
                        if single_msg["text"].startswith(command):

                            self.private_message.message = single_msg
                            # 执行命令
                            await self._distribute(event.api, private_msg.sender.id, event.func, event.params)

                            break
                        else:
                            continue

                    break

            await asyncio.sleep(interval)

    async def _distribute(self, api: str, target: int, callback: Callable, *args):
        """
        distribute callback function bay api parameter.

        :param api: mirai-api-http which is used by command.
        :param target: target group id or friend id.
        :param callback: function which is triggered by command.
        :param args: function`s arguments.
        :return:
        """

        if api == mirai_api.MIRAI_SEND_GROUP_MESSAGE:
            msg = callback(*args)

            session_key = await self.authorize()

            await self.send_group_message(session_key, target, msg, "Plain")

            await self.release(session_key)
        elif api == mirai_api.MIRAI_SEND_GROUP_MESSAGE_WITH_QUOTE:

            # msg = callback(*args)
            #
            # session_key = await self.authorize()
            #
            # await self.send_group_message(session_key, target, msg, "Plain")
            #
            # await self.release(session_key)

            pass

    async def send_group_message(self,
                                 session_key,
                                 target: int,
                                 message_type: str,
                                 message_text: str):
        """发送群消息事件"""

        message_chain = {
            "type": message_type,
            "text": message_text
        }

        data = {
            "sessionKey": session_key,
            "target": target,
            "messageChain": message_chain
        }

        url = self.url + URL.MIRAI_SEND_GROUP_MESSAGE_URL

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(data)) as response:
                print('发送群消息')

    async def send_group_message_with_quote(self,
                                            session_key,
                                            target: int,
                                            message_type: str,
                                            message_text: str,
                                            quote: int):

        """发送带引用的群消息事件"""

        message_chain = {
            "type": message_type,
            "text": message_text
        }

        data = {
            "sessionKey": session_key,
            "target": target,
            "messageChain": message_chain,
            "quote": quote
        }

        url = self.url + URL.MIRAI_SEND_GROUP_MESSAGE_URL

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(data)) as response:
                print('发送群消息')
