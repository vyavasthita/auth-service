from uuid import uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import SessionStatus, User
from src.api.repos import AuthRepository, IAuthRepository, ISessionRepository, SessionRepository
from src.utils import JWTUtils, Security, TokenClaims

from .auth_decorators import is_active_token, is_new_user, is_valid_token, is_valid_user
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

    @is_new_user
    async def register(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
    ) -> User:
        """Register a new user."""
        user_id = uuid4().bytes

        user = User(
            user_id=user_id,
            username=username,
            password=Security.hash_password(password),
        )
        await self.auth_repository.save(db_session, user)

        return user

    @is_valid_user
    async def login(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
        **kwargs,
    ) -> str:
        """Authenticate a user and return a JWT token."""
        user: User = kwargs["user"]
        claims = TokenClaims.for_user(user)
        token = JWTUtils.generate_auth_token(claims=claims.to_payload())

        await self.session_repository.save(db_session, token, claims.jti, SessionStatus.ACTIVE, user.user_id)

        return token

    @is_active_token
    @is_valid_token
    async def validate_token(
        self,
        db_session: AsyncSession,
        token: str,
        user_id: bytes,
        **kwargs,
    ) -> User:
        """Validate a JWT token and return the user if valid."""
        user = kwargs.get("user")
        self.logger.debug(f"validate_token got user: {user}")
        return user
