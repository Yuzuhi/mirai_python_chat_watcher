"""mirai"""
from typing import Callable, Dict, Optional, Tuple
from pydantic import BaseModel


class CommandManagement:
    """接收消息中的命令并"""

    def __init__(self):
        self.command_dict: Dict[str, Callable] = dict()

    def add(self, command_dict: Dict[str, Callable], **kwargs):
        """添加命令与对应的func"""
        for k, func in command_dict.items():
            if callable(func):
                self.command_dict[k] = func

        if kwargs:
            for k, func in kwargs.items():
                if callable(func):
                    self.command_dict[k] = func

    def to_dict(self) -> Dict[str, Callable]:
        return self.command_dict


class Command(BaseModel):
    command: str
    api: str
    func: Optional[Callable]
    params: Optional[Tuple]
    use_group_message_param: bool
    use_friend_message_param: bool
    # use_in_friend_chat: bool
    # use_in_group_chat: bool
