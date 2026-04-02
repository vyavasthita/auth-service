from fastapi import status
from .base_exception import BaseException


class DBException(BaseException):
    def __init__(self, message: str = "Internal Server Error."):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


class DBIntegrityException(BaseException):
    def __init__(self, message: str = "Data integrity violation."):
        super().__init__(status.HTTP_409_CONFLICT, message)


class DBOperationalException(BaseException):
    def __init__(self, message: str = "Database unavailable."):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, message)
