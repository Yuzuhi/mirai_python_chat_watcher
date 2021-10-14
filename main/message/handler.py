import asyncio
import json
import os
from collections import deque
from typing import Callable, Dict, Optional, Tuple, Any, Union, Iterable

import aiohttp

from main.api import url as URL

from main.api.api import MIRAI_SEND_GROUP_MESSAGE

from main.message.base import MessageBase
from modles.command import Command
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
        # 创建一个群与命令的映射
        self.group_command_mapping: Dict[int, Dict[str, Command]] = dict()
        # 获取当前机器人所加入的群列表
        groups = self.get_groups()
        for group in groups:
            # 加载所有群号
            self.group_command_mapping.setdefault(group, dict())

        # 当前循环中的群消息
        self.group_message: Optional[SingleGroupMessage] = None
        # 当前循环中的好友消息
        self.private_message: Optional[SinglePrivateMessage] = None

    async def listen(
            self, group_msg_buffer: deque,
            friend_msg_buffer: deque,
            group_chat_commands: Dict[str, Command],
            private_chat_commands: Dict[str, Command],
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

            self.group_message = SingleGroupMessage(
                sender=group_msg.sender,
                message=dict()
            )

            self.private_message = SinglePrivateMessage(
                sender=private_msg.sender,
                message=dict()
            )

            if group_msg:

                for command, event in group_chat_commands.items():
                    # 检查命令是否匹配
                    if not event.command.startswith(command):
                        continue
                    # 检查是否允许此命令在收到消息的群响应
                    if isinstance(event.targetGroup, Iterable):
                        for group in event.targetGroup:
                            if group_msg.sender.group.id != group:
                                continue
                        else:
                            continue
                    elif isinstance(event.targetGroup, int):
                        if group_msg.sender.group.id != event.targetGroup:
                            continue

                    if isinstance(event.targetGroup, Iterable):
                        for group in event.targetGroup:
                            if group == group_msg.sender.group.id:
                                # 如果发现收到命令的群被允许在此群响应命令，则中断检查
                                break
                        else:
                            # 当前命令不允许在此群执行
                            continue

                    # 查看收到命令的群是否被允许在此群响应命令
                    if event.targetGroup != "*" or event.targetGroup != group_msg.sender.group.id:
                        continue

                    for msg in group_msg.message_chain:
                        self.group_message.message = msg

                        # 匹配到命令,执行函数
                        if msg["text"].startswith(event.command):
                            for target in event.targetGroup:
                                await self._distribute(event.api, target, event.func, event.params)

                    break

            if private_msg:
                for command, event in private_chat_commands.items():
                    for msg in private_msg.message_chain:
                        self.private_message.message = msg

                        # 匹配到命令,执行函数
                        if msg["text"].startswith(event.command):
                            await self._distribute(event.api, private_msg, event.func, event.params)

    async def _distribute(self, api: str, target: int, callback: Callable, *args):
        """
        distribute callback function bay api parameter.

        :param api: mirai-api-http which is used by command.
        :param target: target group id or friend id.
        :param callback: function which is triggered by command.
        :param args: function`s arguments.
        :return:
        """

        if api == MIRAI_SEND_GROUP_MESSAGE:
            msg = callback(*args)

            session_key = self.authorize()

            # sending_info = SendGroupMessageEvent(
            #     target=target,
            #     quote=False,
            #     message=Message(
            #         type="Plain",
            #         text=msg
            #     )
            #
            # )

            await self.send_group_message(session_key, target, msg, "Plain")

    async def send_group_message(self, session_key, target: int, message_type: str, message_text: str,
                                 quote: bool = False):
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

    def get_groups(self) -> List[int]:

    def add_commands(self, command: str,
                     api: str,
                     target_group: Union[str, int, Iterable[int]],
                     func: Optional[Callable] = None,
                     prefix: str = "/",
                     use_in_private_chat: bool = False,
                     *args) -> None:

        if isinstance(target_group, str):
            if target_group != "*":
                raise ValueError("""pass "*" for all group,
                pass integer group id for specific group,
                or pass a bunch of group id for a specific groups""")

        """为事件循环添加命令"""
        command_model = Command(
            command=prefix + command,
            api=api,
            func=func,
            targetGroup=target_group,
            use_in_private_chat=use_in_private_chat,
            params=args,
        )

        self.commands[command_model.command] = command_model
