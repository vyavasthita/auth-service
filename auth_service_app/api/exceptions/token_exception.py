from api.exceptions.base_exception import BaseException

class InvalidTokenException(BaseException):
    def __init__(self, message: str = None):
        super().__init__(status_code=401, message="Invalid or expired token.")
