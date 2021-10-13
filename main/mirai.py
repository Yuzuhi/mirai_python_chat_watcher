from main.message.handler import CommandHandler
from main.message.receiver import MessageReceiver
from modles.command import Command

from typing import Union, Callable, Dict
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
        # 保存用于群聊的命令
        self.group_chat_commands: Dict[str, Command] = dict()
        # 保存用于好友聊天的命令
        self.friend_chat_commands: Dict[str, Command] = dict()

    async def listen(self, interval: float = 0.5):
        """开启miraiBot"""

        # 创建事件循环
        # 将接受message的事件加入到事件循环中
        task =
        # 将处理command的事件加入到事件循环中
        pass

    def add_command(
            self,
            api: str,
            func: Callable,
            command: str,
            prefix: str = "/",
            *args,
            use_group_message_param: bool = True,
            use_friend_message_param: bool = True,
            use_in_group_chat: bool = False,
            use_in_friend_chat: bool = False
    ) -> bool:
        """

        :param api: 希望使用的mirai-api-http中的api，目前提供如下api:
                    [
                    "memberList",获取bot指定群中的成员列表
                    "groupList", 获取bot的群列表
                    "fetchLatestMessage", 即获取最新的消息，获取消息后从队列中移除
                    ]

        :param func: your function
                    [noticed]
                    if your function return a string value,
                    it would be sent to the group where received the command you defined.

        :param command: the command which is used to trigger your function.
        :param prefix: the string which would help bot to know the real command.

        :param args: the arguments used in your function
        :param use_group_message_param: if group_message_param is used in your function ,you can pass True,
                                        if you are not sure pass True.

        :param use_friend_message_param: if friend_message_param is used in your function ,you can pass True,
                                        if you are not sure pass True.

        :param use_in_friend_chat: when get command from friend_chat , trigger function if this param is True.
        :param use_in_group_chat: when get command from group_chat , trigger function if this param is True.
        """
        if not prefix:
            raise ValueError("you must set a prefix")

        if not use_in_friend_chat and use_in_group_chat:
            return False

        full_command = prefix + command

        new_command = Command(
            command=full_command,
            api=api,
            func=func,
            params=args,
            use_group_message_param=use_group_message_param,
            use_friend_message_param=use_friend_message_param,
        )

        if use_in_friend_chat:
            self.friend_chat_commands[full_command] = new_command

        if use_in_group_chat:
            self.group_chat_commands[full_command] = new_command

        return True
