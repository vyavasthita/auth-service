from uuid import uuid4
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from src.api.dependencies.config_dependency import Config
from src.utils import Security, JWTUtils
from src.utils.email_validator import email_format_validator
from src.api.models import User
from src.api.repos import IAuthRepository, AuthRepository
from .auth_service import AuthService


class AuthServiceImpl(AuthService):
    """Implementation of the AuthService for user registration and login."""

    def __init__(
        self,
        auth_repository: IAuthRepository = Depends(AuthRepository),
    ):
        super().__init__(auth_repository)

    @email_format_validator
    @AuthService.is_new_user
    async def register(
        self,
        db_session: AsyncSession,
        email: str,
        name: str,
        password: str,
        phone_number: str,
    ) -> User:
        """Register a new user in the system."""
        user = User(
            id=uuid4().bytes,
            name=name,
            email=email,
            password=Security.hash_password(password),
            phone_number=phone_number,
        )

        return await self.auth_repository.save(db_session, user)

    @email_format_validator
    @AuthService.is_valid_user
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        """Authenticate a user and return a JWT token."""
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config().TOKEN_EXPIRE_MINUTES)
        claims = {"sub": email, "exp": expire}
        return JWTUtils.generate_auth_token(claims=claims)

    @AuthService.is_valid_token
    async def validate_token(
        self,
        db_session: AsyncSession,
        token: str,
        **kwargs,
    ) -> User:
        """Validate a JWT token and return the user if valid."""
        self.logger.debug(f"validate_token called with token: {token}")
        user = kwargs.get('user')
        self.logger.debug(f"validate_token got user: {user}")
        return user
