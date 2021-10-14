from typing import Callable, Iterable
from pydantic import BaseModel

a = (1, 2, 3)

print(isinstance(a, Iterable))
