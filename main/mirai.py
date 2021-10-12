from main.message.handler import CommandHandler
from modles.recevier import MessageReceiver
from typing import Union
from collections import deque


class MiraiBot:

    def __init__(self, url: str, port: int, auth_key: str, bot_qq: int, buffer_size: int = 10):
        if buffer_size < 1:
            raise ValueError("buffer_size must be greater than 1")
        # 用于通过mirai-api-http取到qq消息
        self.message_receiver = MessageReceiver(url, port, auth_key, bot_qq)
        # 用于加载命令
        self.command_handler = CommandHandler(url, port, auth_key, bot_qq)
        # 用于接受群消息的缓冲区
        self.group_msg_buffer = deque(maxlen=buffer_size)
        # 用于接受好友消息的缓冲区
        self.friend_msg_buffer = deque(maxlen=buffer_size)

    async def listen(self, interval: float = 0.5):
        """开启miraiBot"""

        # 创建事件循环
        # 将接受message的事件加入到事件循环中
        # 将处理command的事件加入到事件循环中
        pass

    def add_command(self):
        """添加命令与回调函数"""
        i
