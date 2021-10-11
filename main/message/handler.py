import json
from typing import Callable, Dict, Optional, Tuple, Any

import aiohttp

from main.message.base import MessageBase
from modles.command import Command
from modles.constant import GroupMessageType
from modles.events import SendGroupMessageEvent
from modles.messages import GroupMessage
from utils.queue import Queue


class MessageHandler(MessageBase):
    """从缓存区读取mirai bot的消息，并通过自定义的方法来处理并通过http协议发送给mirai-api-http"""

    def __init__(self, url: str, port: str, auth_key: str, bot_qq: int):

        super().__init__(url, port, auth_key, bot_qq)

        self.commands: Dict[str, Command] = dict()

    async def listen(self, queue: Queue, interval: float = 0.5):
        while True:
            msg: GroupMessage = queue.pop()
            if msg.type != GroupMessageType:
                continue

            for received_msg in msg.message_chain.messages:
                for command in self.commands.keys():
                    if received_msg["text"] != command:
                        continue
                    # 匹配到命令，执行函数

                    msg = self.commands[command].func(*self.commands[command].params)
                    if msg:
                        # 发送消息
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

    def add_commands(self, command: str,
                     api: str,
                     func: Optional[Callable] = None,
                     params: Optional[Tuple] = None,
                     prefix: str = "/",
                     command_type: str = "full") -> None:

        """为事件循环添加命令"""
        command_model = Command(
            prefix=prefix,
            command=command,
            api=api,
            func=func,
            params=params,
            command_type=command_type
        )

        self.commands[command_model.prefix + command_model.command] = command_model
        for c in params:
            if isinstance(c, Command):
                self.commands[command_model.prefix + command_model.command] = command_model
