from abc import ABC, abstractmethod
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import User
from api.repositories import AuthRepository
from api.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)

class AuthService(ABC):
    async def _check_user(self, db_session: AsyncSession, email: str) -> User | None:
        return await self.auth_repository.find_by_email(db_session, email=email)

    @staticmethod
    def is_new_user(func):
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, *args, **kwargs):
            user = await self._check_user(db_session, email)

            if user is not None:
                from api.exceptions import UserAlreadyExistsException
                raise UserAlreadyExistsException(email=email)
            return await func(self, db_session, email, *args, **kwargs)
        
        return wrapper

    @staticmethod
    def is_valid_user(func):
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, **kwargs):
            user = await self._check_user(db_session, email)

            if user is None:
                from api.exceptions import UserNotFoundException
                raise UserNotFoundException(email=email)
            kwargs['user'] = user
            return await func(self, db_session, email, **kwargs)
        return wrapper

    def __init__(self, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    @property
    def auth_repository(self) -> AuthRepository:
        return self._auth_repository

    @auth_repository.setter
    def auth_repository(self, auth_repository: AuthRepository) -> None:
        self._auth_repository = auth_repository

    @abstractmethod
    async def register(
        self,
        db_session: AsyncSession,
        name: str,
        email: str,
        password: str,
        phone_number: str,
    ) -> User:
        raise NotImplementedError("Method 'register' needs implementation.")

    @abstractmethod
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        raise NotImplementedError("Method 'login' needs implementation.")