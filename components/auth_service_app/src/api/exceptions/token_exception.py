from .base_exception import BaseException


class InvalidTokenException(BaseException):
    def __init__(self, message: str = "Invalid or expired token."):
        super().__init__(status_code=401, message=message)
