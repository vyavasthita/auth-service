from uuid import uuid4
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from api.dependencies import Config
from api.utils import Security, JWTUtils
from api.utils.email_validator import email_format_validator
from api.models import User
from api.repositories import AuthRepository, AuthRepositoryImpl
from .auth_service import AuthService


class AuthServiceImpl(AuthService):
    """
    Implementation of the AuthService for user registration and login.
    """

    def __init__(
        self,
        auth_repository: AuthRepository = Depends(AuthRepositoryImpl),
    ):
        """
        Initialize the AuthServiceImpl with an AuthRepository dependency.
        """
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
        """
        Register a new user in the system.
        Checks for existing user before creating.
        """

        user = User(id=uuid4().bytes,
                    name=name,
                    email=email,
                    password=Security.hash_password(password),
                    phone_number=phone_number)
        
        return await self.auth_repository.save(db_session, user)

    @email_format_validator
    @AuthService.is_valid_user
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        """
        Authenticate a user and return a JWT token.
        User existence and password validity are checked by the decorator.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config().TOKEN_EXPIRE_MINUTES)

        claims = {"sub": email, "exp": expire}

        return JWTUtils.generate_auth_token(claims=claims)