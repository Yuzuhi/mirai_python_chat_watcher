from typing import Callable
from pydantic import BaseModel


class Got(BaseModel):
    id: int


def add(which, func, *args, use_got: bool = True):
    my_p = "xxx"
    g = Got(id=5)
    if which == 1:
        pass
    if which == 2:
        pass
    if which == 3:
        if use_got:
            wrapper(func,g, *args)
        if not use_got:
            wrapper(func,*args)


def wrapper(func, my_p, *args):
    msg = func(my_p, *args)
    api(msg)


def api(msg):
    print(f"发送消息:{msg}")


def inner(g: Got, other):
    print("do sth")
    return "finish"


add(3, inner, 15, use_got=True)
