from typing import Callable, Optional, List, Dict, Any

from pydantic import BaseModel

def aaa(func,*args,**kwargs):

    return func(*args,**kwargs)


class Message(BaseModel):
    type: str = "Plain"
    text: str = ""

    # class Config:
    #     json_encoders = {
    #
    #     }


class EventBase(BaseModel):
    """
    prefix:命令前缀
    command:命令
    func:接受命令后执行的函数
    api:发送的目标api
    """
    prefix: str = "/"
    command: str
    api: str
    func: Optional[Callable]
    param: Optional[Any]
    # callable:


class SendGroupMessageEvent(EventBase):
    """
    target:目标群群号
    quote:引用一条消息的messageId进行回复
    message:单次发送的消息
    messageChain:消息链，是一个消息对象构成的列表
    """
    target: int
    quote: Optional[int]
    message: Message = Message()


def test(x, y, z):
    return str(x + y + z)

print(aaa(test,1,2,3))


m = SendGroupMessageEvent(
    command="haha",
    api="hehe",
    target=123,
    func=test,
    param=(5, 4, 3)
)

m.message.text = m.func(*m.param)
print(m.message)
