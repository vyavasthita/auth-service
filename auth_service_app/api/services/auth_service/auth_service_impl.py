import secrets
from functools import wraps
from typing import Any, Callable, Optional
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from api.models import User
from api.repositories import AuthRepository, AuthRepositoryImpl
from .auth_service import AuthService


def is_user_exist(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(
        self,
        db_session: AsyncSession,
        email: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        user: Optional[User] = await self.auth_repository.find_by_email(
            db_session,
            email=email,
        )
        if user is None:
            raise UserNotFoundException(email)

        kwargs.setdefault("user", user)
        return await func(self, db_session, email, *args, **kwargs)

    return wrapper


class AuthServiceImpl(AuthService):
    def __init__(
        self,
        auth_repository: AuthRepository = Depends(AuthRepositoryImpl),
    ):
        super().__init__(auth_repository)

    async def __is_user_exists(self, db_session: AsyncSession, email: str) -> bool:
        user: Optional[User] = await self.auth_repository.find_by_email(
            db_session,
            email=email,
        )
        return user is not None

    def _generate_auth_token(self) -> str:
        return secrets.token_urlsafe(32)

    async def register(
        self,
        db_session: AsyncSession,
        name: str,
        email: str,
        password: str,
        phone_number: str,
    ) -> User:
        if await self.__is_user_exists(db_session, email=email):
            raise UserAlreadyExistsException(email=email)

        user = User()

        user.id = uuid4().bytes
        user.name = name
        user.email = email
        user.password = password
        user.phone_number = phone_number

        return await self.auth_repository.save(db_session, user)

    @is_user_exist
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
        *,
        user: Optional[User] = None,
    ) -> str:
        if user is None:
            raise UserNotFoundException(email)

        if user.password != password:
            raise InvalidCredentialsException()

        return self._generate_auth_token()