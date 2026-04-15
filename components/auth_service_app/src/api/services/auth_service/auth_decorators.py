from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.api.models import SessionStatus, UserSession
from src.utils import Security


def is_new_user(func):
    """Decorator to ensure the user does not already exist before registration."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, username: str, *args, **kwargs):
        user = await self._check_user(db_session, username)

        if user is not None:
            raise UserAlreadyExistsException(username=username)

        return await func(self, db_session, username, *args, **kwargs)

    return wrapper


def is_valid_user(func):
    """Decorator to ensure the user exists and password is valid before login."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, username: str, password: str, **kwargs):
        user = await self._check_user(db_session, username)

        if user is None:
            raise UserNotFoundException(username=username)

        if not Security.verify_password(password, user.password):
            raise InvalidCredentialsException()

        kwargs["user"] = user

        return await func(self, db_session, username, password, **kwargs)

    return wrapper


def is_active_token(func):
    """Decorator to ensure the token has an active session in the database."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, token: str, user_id: bytes, **kwargs):
        session: UserSession | None = await self.session_repository.find_by_user_and_token(db_session, user_id, token)

        if session is None or session.status != SessionStatus.ACTIVE:
            self.logger.info("Token session is not active.")
            raise InvalidTokenException()

        return await func(self, db_session, token, user_id, **kwargs)

    return wrapper
