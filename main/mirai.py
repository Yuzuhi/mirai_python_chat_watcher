from main.message.handler import CommandHandler
from main.message.receiver import MessageReceiver
from modles.command import Command, PrivateCommand, GroupCommand

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
        # 保存各个群允许被使用的命令的字典
        self.group_command_mapping: Dict[int, Dict[str, GroupCommand]] = dict()
        # 获取当前机器人所加入的群列表
        groups = self.command_handler.get_groups()
        for group in groups:
            # 初始化所有群保存命令的字典
            self.group_command_mapping.setdefault(group, dict())

        # 保存允许被用于私聊中的命令的字典
        self.private_command_mapping: Dict[str, PrivateCommand] = dict()
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

    def add_commands(self,
                     command: str,
                     api: str,
                     func,
                     *args,
                     target_group: Union[str, int, Iterable[int]] = "*",
                     prefix: str = "/",
                     use_in_private_chat: bool = False,
                     use_in_group_chat: bool = False) -> None:

        """
        为事件循环添加命令
        :param command:the command which is used to trigger your function.
        :param api:http-api which you want to use from mirai-api-http，the following api are now available:

                    "memberList",获取bot指定群中的成员列表
                    "groupList", 获取bot的群列表
                    "fetchLatestMessage", 即获取最新的消息，获取消息后从队列中移除

        :param args:the arguments used in your function.
        :param target_group:pass "*" for all group,pass group number or a bunch of group number to
                                use this function in specific group.
        :param func:your function
                    [noticed]
                    if your function return a string value,
                    it would be sent to the group where received the command you defined.

        :param prefix:the string which would help bot to know the real command.
        :param use_in_private_chat:to let bot response your command in private chat.
        :param use_in_group_chat:to let bot response your command in group chat.
        """

        if not use_in_group_chat and not use_in_private_chat:
            raise ValueError("""this command should be assigned to be used in group or private""")

        if isinstance(target_group, str) and target_group != "*":
            raise ValueError("""pass "*" for all group,
                            pass integer group id for specific group,
                            or pass a bunch of group id for a specific groups""")

        command = prefix + command

        if use_in_private_chat:
            private_command = PrivateCommand(
                command=command,
                api=api,
                func=func,
                params=args,
            )

            self.private_command_mapping[command] = private_command

        if use_in_group_chat:

            group_command = GroupCommand(
                command=command,
                api=api,
                func=func,
                params=args,
            )

            if isinstance(target_group, str):
                for command_dict in self.group_command_mapping.values():
                    command_dict[group_command.command] = group_command

            elif isinstance(target_group, Iterable):
                for g in target_group:
                    if self.group_command_mapping.get(g):
                        self.group_command_mapping[g].update(
                            {group_command.command: group_command}
                        )

            elif isinstance(target_group, int):
                if self.group_command_mapping.get(target_group):
                    self.group_command_mapping[target_group].update(
                        {group_command.command: group_command}
                    )

    def add_group_commands(self,
                           c: str,
                           api: str,
                           target_group,
                           prefix: str = "/", ):

        def wrapper(func):

            def deco(*args, **kwargs):

                if isinstance(target_group, str) and target_group != "*":
                    raise ValueError("""pass "*" for all group,
                                    pass integer group id for specific group,
                                    or pass a bunch of group id for a specific groups""")

                command = prefix + c

                group_command = GroupCommand(
                    command=command,
                    api=api,
                    func=func,
                    params=args,
                )

                if isinstance(target_group, str):
                    for command_dict in self.group_command_mapping.values():
                        command_dict[group_command.command] = group_command

                elif isinstance(target_group, Iterable):
                    for g in target_group:
                        if self.group_command_mapping.get(g):
                            self.group_command_mapping[g].update(
                                {group_command.command: group_command}
                            )

                elif isinstance(target_group, int):
                    if self.group_command_mapping.get(target_group):
                        self.group_command_mapping[target_group].update(
                            {group_command.command: group_command}
                        )

            return deco

        return wrapper
