from typing import List

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


class GroupMessage(BaseModel):
    type: str = "GroupMessage"
    sender: GroupSender
    message_chain: MessageChain

