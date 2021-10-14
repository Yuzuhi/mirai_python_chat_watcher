"""base class of MessageHandler&MessageReceiver"""
import asyncio
import json
from typing import List

import aiohttp
import requests

from exceptions.exc import AuthorizeException
from main.api import url


class MessageBase:

    def __init__(self, url: str, port: int, auth_key: str, bot_qq: int):

        # miral bot项目的url
        self.url: str = f"{url}:{port}"
        # mirai http的auth key
        self.authKey: str = auth_key
        # bot的QQ号
        self.bot_qq: int = bot_qq

    async def authorize(self) -> str:
        # mirai_bot的验证与绑定
        auth_key = {"authKey": self.authKey}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + url.MIRAI_VERIFY_URL, data=json.dumps(auth_key)) as response:
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
            async with session.post(self.url + url.MIRAI_BIND_URL, data=json.dumps(data)) as response:
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
            async with session.post(self.url + url.MIRAI_RELEASE_URL, data=json.dumps(data)) as response:
                result = await response.json()

        return result["code"] == 0

    def get_groups(self) -> List[int]:
        """
        获取当前机器人所在的所有群
        read https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/API.md#%E8%8E%B7%E5%8F%96%E7%BE%A4%E5%88%97%E8%A1%A8
        """
        # mirai_bot的验证与绑定
        auth_key = {"authKey": self.authKey}
        response = requests.post(self.url + url.MIRAI_VERIFY_URL, data=json.dumps(auth_key))

        if response.status_code != 0:
            raise AuthorizeException

        session_key = response.json()["session"]

        # bind
        data = {
            "sessionKey": session_key,
            "qq": self.bot_qq
        }

        response = requests.post(self.url + url.MIRAI_BIND_URL, data=json.dumps(data))

        if response.status_code != 0:
            raise AuthorizeException

        # get groups

        response = requests.get(self.url + url.MIRAI_GET_GROUP_LIST_URL % session_key)

        if response.status_code != 0:
            raise AuthorizeException

        # release

        data = {
            "sessionKey": session_key,
            "qq": self.bot_qq
        }

        requests.post(self.url + url.MIRAI_RELEASE_URL, data=json.dumps(data))

        # return groups

        group_list = list()

        groups = response.json()["data"]

        for group in groups:
            group_list.append(group["id"])

        return group_list

