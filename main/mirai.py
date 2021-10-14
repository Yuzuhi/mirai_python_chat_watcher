from main.message.handler import CommandHandler
from main.message.receiver import MessageReceiver
from modles.command import Command

from typing import Union, Callable, Dict, Optional, Iterable
from collections import deque

from modles.messages import GroupMessage, PrivateMessage


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
        self.private_chat_commands: Dict[str, Command] = dict()
        # 当前循环中的群消息
        self.group_message: Optional[GroupMessage] = None
        # 当前循环中的好友消息
        self.private_message: Optional[PrivateMessage] = None

    async def listen(self, interval: float = 0.5):
        """开启miraiBot"""

        # 创建事件循环
        # 将接受message的事件加入到事件循环中

        # 将处理command的事件加入到事件循环中
        pass

    def get_group_message(self) -> Optional[PrivateMessage]:
        return self.command_handler.group_message

    def get_friend_message(self) -> Optional[PrivateMessage]:
        return self.command_handler.private_message

    def add_command(
            self,
            api: str,
            func: Callable,
            command: str,
            target_group: Union[str, int, Iterable[int]],
            *args,
            prefix: str = "/",
            use_in_private_chat: bool = False,
    ):
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
        :param target_group: pass "*" for all group,pass group number or a bunch of group number to
                                use this function in specific group.

        :param use_in_private_chat: to let bot response your command in private chat.
        """
        if not prefix:
            raise ValueError("you must set a prefix")

        full_command = prefix + command

        new_command = Command(
            command=full_command,
            api=api,
            func=func,
            params=args,
            target_group=target_group,
            use_in_private_chat=use_in_private_chat,
        )

        self.group_chat_commands[full_command] = new_command

        if use_in_private_chat:
            self.private_chat_commands[full_command] = new_command
