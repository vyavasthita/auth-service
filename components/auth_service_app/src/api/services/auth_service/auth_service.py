from abc import ABC, abstractmethod
from functools import wraps
import jwt
import time
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils import Security, JWTUtils
from src.api.models import User
from src.api.repos import IAuthRepository
from src.api.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from src.utils import AuthServiceLogger


class AuthService(ABC):
    """Abstract base class for authentication service."""

    def __init__(self, auth_repository: IAuthRepository):
        self.logger = AuthServiceLogger.get_logger()
        self._auth_repository = auth_repository

    @property
    def auth_repository(self) -> IAuthRepository:
        return self._auth_repository

    @auth_repository.setter
    def auth_repository(self, auth_repository: IAuthRepository) -> None:
        self._auth_repository = auth_repository

    async def _check_user(self, db_session: AsyncSession, email: str) -> User | None:
        return await self.auth_repository.find_by_email(db_session, email=email)

    @staticmethod
    def is_new_user(func):
        """Decorator to ensure the user does not already exist before registration."""
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, *args, **kwargs):
            user = await self._check_user(db_session, email)

            if user is not None:
                raise UserAlreadyExistsException(email=email)

            return await func(self, db_session, email, *args, **kwargs)

        return wrapper

    @staticmethod
    def is_valid_user(func):
        """Decorator to ensure the user exists and password is valid before login."""
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, password: str):
            user = await self._check_user(db_session, email)

            if user is None:
                raise UserNotFoundException(email=email)

            if not Security.verify_password(password, user.password):
                raise InvalidCredentialsException()

            return await func(self, db_session, email, password)

        return wrapper

    @staticmethod
    def is_valid_token(func):
        """Decorator to ensure the token is valid."""
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, token: str, **kwargs):
            self.logger.debug("Validating token.")

            try:
                claims = JWTUtils.decode_auth_token(token)
                self.logger.debug(f"validate_token claims: {claims}")
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                self.logger.debug("Token is invalid.")
                raise InvalidTokenException()

            exp = claims.get('exp')

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

            kwargs['user'] = user

            return await func(self, db_session, token, **kwargs)

        return wrapper

    @abstractmethod
    async def register(
        self,
        db_session: AsyncSession,
        email: str,
        name: str,
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

    @abstractmethod
    async def validate_token(
        self,
        db_session: AsyncSession,
        token: str,
    ) -> User:
        raise NotImplementedError("Method 'validate_token' needs implementation.")
