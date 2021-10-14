from typing import List, Dict

from pydantic import BaseModel


class MessageChain(BaseModel):
    messages: List


class GroupInfo(BaseModel):
    id: int
    name: str
    permission: str


class GroupSender(BaseModel):
    id: int
    memberName: str
    specialTitle: str
    permission: str
    joinTimestamp: int
    lastSpeakTimestamp: int
    muteTimeRemaining: int
    group: GroupInfo


class FriendSender(BaseModel):
    id: int
    nickname: str
    remark: str


class GroupMessage(BaseModel):
    type: str = "GroupMessage"
    sender: GroupSender
    message_chain: List[Dict[str, str]]


class SingleGroupMessage(BaseModel):
    type: str = "GroupMessage"
    sender: GroupSender
    message: Dict[str, str]


class PrivateMessage(BaseModel):
    type: str = "FriendMessage"
    sender: GroupSender
    message_chain: List[Dict[str, str]]


class SinglePrivateMessage(BaseModel):
    type: str = "FriendMessage"
    sender: GroupSender
    message: Dict[str, str]
