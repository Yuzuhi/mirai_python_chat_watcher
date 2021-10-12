from typing import Any
from collections import deque


class Queue:
    def __init__(self, maxsize: int = 10):
        self.__list = []
        self.maxsize = maxsize

    def append(self, item: Any) -> bool:
        if len(self.__list) < self.maxsize:
            self.__list.append(item)
            return True

    def pop(self) -> Any:
        return self.__list.pop()

