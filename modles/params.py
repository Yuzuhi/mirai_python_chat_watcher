from pydantic import BaseModel


class Params(BaseModel):
    """你可以获取的参数类"""
    qq_id: int
