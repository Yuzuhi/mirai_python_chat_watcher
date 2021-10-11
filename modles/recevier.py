"""
通过http通信访问mirai-bot的http api，实时接收群内消息，并且对不同的关键字做不同反应
"""
import asyncio
import json
from typing import List

import aiohttp

from exceptions.exc import AuthorizeException
from main.message import const



class MessageReceiver:

    def __init__(self, url: str, port: str, auth_key: str, bot_qq: int, command_prefix: str = "/"):

        # miral bot项目的url
        self.url: str = url + ":" + port
        # mirai http的auth key
        self.authKey: str = auth_key
        # bot的QQ号
        self.bot_qq: int = bot_qq
        # 目标群的群号,用,分割
        self.groups: List[int] = await self.get_groups()
        # mirai_bot命令识别符
        self.command_prefix: str = command_prefix

    async def authorize(self) -> str:
        # mirai_bot的验证与绑定
        auth_key = {"authKey": self.authKey}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + const.MIRAI_VERIFY, data=json.dumps(auth_key)) as response:
                print('generating session')
                result = await response.json()
        if result.get('code') != 0:
            raise AuthorizeException

        session_key = result['session']
        # bind
        data = {
            "sessionKey": session_key,
            "qq": self.bot_qq
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + const.MIRAI_BIND, data=json.dumps(data)) as response:
                print('binding')
                result = await response.json()

        if result.get('code') != 0:
            raise AuthorizeException
        else:
            return session_key

    async def release(self, session_key: str) -> bool:
        """释放mirai_bot的session_key"""

        data = {
            "sessionKey": session_key,
            "qq": self.bot_qq
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + const.MIRAI_RELEASE, data=json.dumps(data)) as response:
                result = await response.json()

        return result["code"] == 0

    async def get_groups(self) -> List[int]:
        """
        获取当前机器人所在的所有群
        read https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/API.md#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%88%97%E8%A1%A8
        """
        groups = list()

        try:
            session_key = await self.authorize()

        except AuthorizeException:
            await asyncio.sleep(0.01)
            session_key = await self.authorize()

        if session_key:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url + ("/groupList?sessionKey=%s" % session_key)) as response:
                    result = await response.json()

            if result.get('code') != 0:
                await self.release(session_key)
                raise AuthorizeException
            else:
                for group in result["data"]:
                    groups.append(int(group["id"]))

        await self.release(session_key)
        return groups

    def in_group(self, group_id: int) -> bool:
        return group_id in self.groups

    async def listen(self):
        """mirai_bot消息监听"""
        pass

    def add_event(self,):
        """配置mirai_bot的监听事件"""


    async def send(self, msg: str, session_key: str):
        # 向qq群发送消息
        for group in self.groups:

        data = {
            "sessionKey": session_key,
            "target": target,
            "messageChain": [
                {"type": "Plain", "text": message}
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url + "/sendGroupMessage", data=json.dumps(data)) as response:
                print('发送群消息')

    async def send_message(self, message: str):
        # Authorize
        auth_key = {"authKey": self.authKey}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + "/auth", data=json.dumps(auth_key)) as response:
                print('generating session')
                result = await response.json()
        if result.get('code') != 0:
            print("ERROR@auth")
            print(result.text)
            exit(1)

        # Verify
        session_key = result['session']
        data = {"sessionKey": session_key, "qq": self.bot_qq}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + "/verify", data=json.dumps(data)) as response:
                print('verifying session')
                result = await response.json()

        if result.get('code') != 0:
            print("ERROR@verify")
            print(result.text)
            exit(2)
        data = {
            "sessionKey": session_key,
            "target": target,
            "messageChain": [
                {"type": "Plain", "text": message}
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url + "/sendGroupMessage", data=json.dumps(data)) as response:
                print('发送群消息')

        # release

        data = {
            "sessionKey": session_key,
            "qq": self.bot_qq
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + "/release", data=json.dumps(data)) as response:
                print('释放session')
