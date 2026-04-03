from fastapi import status

from .base_exception import BaseException


class RoleNotFoundException(BaseException):
    def __init__(self, role: str):
        super().__init__(status.HTTP_404_NOT_FOUND, f"Role with '{role}' not found.")


class RoleAlreadyExistsException(BaseException):
    def __init__(self, role: str):
        self.role = role
        super().__init__(status.HTTP_409_CONFLICT, f"Role with '{role}' already exists.")
