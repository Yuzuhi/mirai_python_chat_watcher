from typing import List, Dict

from pydantic import BaseModel


class MessageChain(BaseModel):
    messages: List


class GroupSender(BaseModel):
    id: int
    memberName: str
    specialTitle: str
    permission: str
    joinTimestamp: int
    lastSpeakTimestamp: int
    muteTimeRemaining: int
    # "group": {
    #     "id": 321,
    #     "name": "",
    #     "permission": "MEMBER",
    # },


class FriendSender(BaseModel):
    id: int
    nickname: str
    remark: str


class GroupMessage(BaseModel):
    type: str = "GroupMessage"
    sender: GroupSender
    message_chain: List[Dict[str, str]]


class FriendMessage(BaseModel):
    type: str = "FriendMessage"
    sender: GroupSender
    message_chain: List
