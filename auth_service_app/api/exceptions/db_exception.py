from fastapi import status
from .base_exception import BaseException


class DBConnectionException(BaseException):
    def __init__(self):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error.")