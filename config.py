import os
from typing import Union
from ipaddress import ip_address

from pydantic import BaseSettings, AnyHttpUrl, IPvAnyAddress


class Settings(BaseSettings):
    DEBUG: bool = True
    MIRAI_HOST: Union[AnyHttpUrl, IPvAnyAddress] = ip_address("http://127.0.0.1")
    MIRAI_PORT: int = 8080
    MIRAI_URL: str = f"{MIRAI_HOST}:{MIRAI_PORT}/"
    MIRAI_QQ: int = 3093454991
    AUTH_KEY: str = "tessa1213"
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))


settings = Settings()
