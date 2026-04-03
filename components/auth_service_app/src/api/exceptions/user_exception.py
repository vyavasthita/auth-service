from fastapi import status

from .base_exception import BaseException


class UserNotFoundException(BaseException):
    def __init__(self, email: str):
        super().__init__(status.HTTP_404_NOT_FOUND, f"User with '{email}' not found.")


class UserAlreadyExistsException(BaseException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(status.HTTP_409_CONFLICT, f"User with '{email}' already exists.")


class InvalidCredentialsException(BaseException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid email or password.")


class EmailFormatException(BaseException):
    def __init__(self, message: str):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


class PhoneNumberAlreadyExistsException(BaseException):
    def __init__(self, phone_number: str):
        super().__init__(status.HTTP_409_CONFLICT, f"Phone number '{phone_number}' is already registered.")
