from abc import ABC, abstractmethod
from functools import wraps
import jwt
import time
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import Security, JWTUtils
from api.models import User
from api.repositories import AuthRepository
from api.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from api.utils import AuthServiceLogger

class AuthService(ABC):
    """
    Abstract base class for authentication service.
    """
    def __init__(self):
        self.logger = AuthServiceLogger.get_logger()

    async def _check_user(self, db_session: AsyncSession, email: str) -> User | None:
        """
        Check if a user exists by email.

        Args:
            db_session (AsyncSession): The database session.
            email (str): The user's email address.

        Returns:
            User | None: The user if found, else None.
        """
        return await self.auth_repository.find_by_email(db_session, email=email)

    @staticmethod
    def is_new_user(func):
        """
        Decorator to ensure the user does not already exist before registration.
        """
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, *args, **kwargs):
            user = await self._check_user(db_session, email)

            if user is not None:
                raise UserAlreadyExistsException(email=email)
            
            return await func(self, db_session, email, *args, **kwargs)
        
        return wrapper

    @staticmethod
    def is_valid_user(func):
        """
        Decorator to ensure the user exists and password is valid before login.
        """
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, email: str, password: str):
            user = await self._check_user(db_session, email)

            if user is None:
                raise UserNotFoundException(email=email)
            
            if not Security.verify_password(password, user.password):
                raise InvalidCredentialsException()
            
            return await func(self, db_session, email, password)
    
    @staticmethod
    def is_valid_token(func):
        """
        Decorator to ensure the token is valid
        """
        @wraps(func)
        async def wrapper(self, db_session: AsyncSession, token: str, **kwargs):
            self.logger.debug(f"Validating token.")
            

            try:
                claims = JWTUtils.decode_auth_token(token)
                self.logger.debug(f"validate_token claims: {claims}")
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                self.logger.debug("Token is invalid.")
                raise InvalidTokenException()

            # Check token expiry manually if not handled by decode_auth_token
            
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

    def __init__(self, auth_repository: AuthRepository):
        """
        Initialize the AuthService with an AuthRepository.

        Args:
            auth_repository (AuthRepository): The authentication repository.
        """
        self._auth_repository = auth_repository

    @property
    def auth_repository(self) -> AuthRepository:
        """
        Get the authentication repository instance.
        Returns:
            AuthRepository: The authentication repository.
        """
        return self._auth_repository

    @auth_repository.setter
    def auth_repository(self, auth_repository: AuthRepository) -> None:
        """
        Set the authentication repository instance.
        Args:
            auth_repository (AuthRepository): The authentication repository.
        """
        self._auth_repository = auth_repository

    @abstractmethod
    async def register(
        self,
        db_session: AsyncSession,
        email: str,
        name: str,
        password: str,
        phone_number: str,
    ) -> User:
        """
        Abstract method to register a new user.
        """
        raise NotImplementedError("Method 'register' needs implementation.")

    @abstractmethod
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        """
        Abstract method to authenticate a user and return a token.
        """
        raise NotImplementedError("Method 'login' needs implementation.")

    @abstractmethod
    async def validate_token(
        self,
        token: str,
    ) -> dict:
        """
        Abstract method to validate a JWT token and return claims or raise exception.
        """
        raise NotImplementedError("Method 'validate_token' needs implementation.")