import time
from functools import wraps

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.utils import JWTUtils, Security


def is_new_user(func):
    """Decorator to ensure the user does not already exist before registration."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, email: str, *args, **kwargs):
        user = await self._check_user(db_session, email)

        if user is not None:
            raise UserAlreadyExistsException(email=email)

        return await func(self, db_session, email, *args, **kwargs)

    return wrapper


def is_valid_user(func):
    """Decorator to ensure the user exists and password is valid before login."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, email: str, password: str, **kwargs):
        user = await self._check_user(db_session, email)

        if user is None:
            raise UserNotFoundException(email=email)

        if not Security.verify_password(password, user.password):
            raise InvalidCredentialsException()

        kwargs["user"] = user

        return await func(self, db_session, email, password, **kwargs)

    return wrapper


def is_valid_token(func):
    """Decorator to ensure the token is valid."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, token: str, **kwargs):
        self.logger.debug("Validating token.")

        try:
            claims = JWTUtils.decode_auth_token(token)
            self.logger.debug(f"validate_token claims: {claims}")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            self.logger.debug("Token is invalid.")
            raise InvalidTokenException() from e

        exp = claims.get("exp")

        if exp is not None:
            now = int(time.time())
            if isinstance(exp, float):
                exp = int(exp)
            if now > exp:
                self.logger.debug("Token is expired.")
                raise InvalidTokenException()

        user = await self._check_user(db_session, claims["sub"])

        if user is None:
            raise UserNotFoundException(email=claims["sub"])

        kwargs["user"] = user

        return await func(self, db_session, token, **kwargs)

    return wrapper
