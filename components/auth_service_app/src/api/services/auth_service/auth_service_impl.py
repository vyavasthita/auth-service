from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.config_dependency import Config
from src.api.exceptions.user_exception import PhoneNumberAlreadyExistsException
from src.api.models import SessionStatus, User
from src.api.models.user_profile import UserProfile
from src.api.repos import AuthRepository, IAuthRepository, ISessionRepository, SessionRepository
from src.utils import JWTUtils, Security
from src.utils.email_validator import email_format_validator

from .auth_decorators import is_new_user, is_valid_token, is_valid_user
from .auth_service import AuthService


class AuthServiceImpl(AuthService):
    """Implementation of the AuthService for user registration and login."""

    def __init__(
        self,
        auth_repository: IAuthRepository = Depends(AuthRepository),
        session_repository: ISessionRepository = Depends(SessionRepository),
    ):
        super().__init__(auth_repository)
        self._session_repository = session_repository

    @property
    def session_repository(self) -> ISessionRepository:
        return self._session_repository

    @session_repository.setter
    def session_repository(self, session_repository: ISessionRepository) -> None:
        self._session_repository = session_repository

    @email_format_validator
    @is_new_user
    async def register(
        self,
        db_session: AsyncSession,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        phone_number: str,
    ) -> User:
        """Register a new user and create their profile."""
        user_id = uuid4().bytes

        user = User(
            user_id=user_id,
            email=email,
            password=Security.hash_password(password),
        )
        await self.auth_repository.save(db_session, user)

        profile = UserProfile(
            user_profile_id=uuid4().bytes,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_id=user_id,
        )
        db_session.add(profile)

        try:
            await db_session.flush()
        except IntegrityError as e:
            await db_session.rollback()
            raise PhoneNumberAlreadyExistsException(phone_number) from e

        user.profile = profile
        return user

    @email_format_validator
    @is_valid_user
    async def login(
        self,
        db_session: AsyncSession,
        email: str,
        password: str,
        **kwargs,
    ) -> str:
        """Authenticate a user and return a JWT token."""
        user: User = kwargs["user"]
        expire = datetime.now(UTC) + timedelta(minutes=Config().TOKEN_EXPIRE_MINUTES)
        claims = {"sub": email, "exp": expire}
        token = JWTUtils.generate_auth_token(claims=claims)

        await self.session_repository.save(db_session, token, SessionStatus.ACTIVE, user.user_id)

        return token

    @is_valid_token
    async def validate_token(
        self,
        db_session: AsyncSession,
        token: str,
        **kwargs,
    ) -> User:
        """Validate a JWT token and return the user if valid."""
        self.logger.debug(f"validate_token called with token: {token}")
        user = kwargs.get("user")
        self.logger.debug(f"validate_token got user: {user}")
        return user
