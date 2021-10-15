from typing import Callable, Iterable
from pydantic import BaseModel

tasks = []


def add_command(api, command):
    def wrapper(func):
        def decorator(*args, **kwargs):
            tasks.append((func, api, command, args))

            # func(*args, **kwargs)

        return decorator

    return wrapper


@add_command("123", 456)
def test(x, y):
    return x * 2 + y * 4


# test(2, 4)

print(tasks)

#
# def say_hello(country):
#     def wrapper(func):
#         def deco(*args, **kwargs):
#             if country == 'china':
#                 print('你好！')
#             elif country == 'america':
#                 print('hello')
#             else:
#                 return
#             func(*args, **kwargs)
#         return deco
#     return wrapper
#
#
# @say_hello('china')
# def chinese():
#     print('我来自中国。')
#
#
# @say_hello('america')
# def america():
#     print('I am from America.')
#
#
# america()
# print('-'*20)
# chinese()
