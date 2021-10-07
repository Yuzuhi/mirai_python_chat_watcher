class AuthorizeException(Exception):
    """mirai_bot认证异常"""

    def __str__(self):
        return "authorize_failed"
