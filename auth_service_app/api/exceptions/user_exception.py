
from fastapi import status
from .base_exception import BaseException


class UserNotFoundException(BaseException):
    def __init__(self, identifier: str):
        super().__init__(status.HTTP_404_NOT_FOUND, f"User with '{identifier}' not found.")


class UserAlreadyExistsException(BaseException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(status.HTTP_409_CONFLICT, f"User with '{self.email}' already exists.")


class InvalidCredentialsException(BaseException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid email or password.")

class EmailFormatException(BaseException):
    def __init__(self, email: str):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Email '{email}' is invalid")