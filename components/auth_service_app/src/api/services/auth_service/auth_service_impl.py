from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.token_exception import InvalidTokenException
from src.api.exceptions.user_exception import FailToCreateUserException
from src.api.models import Role, SessionStatus, User
from src.api.repos import (
    AuthRepository,
    IAuthRepository,
    IRoleRepository,
    ISessionRepository,
    IUserRepository,
    IUserRoleRepository,
    RoleRepository,
    SessionRepository,
    UserRepository,
    UserRoleRepository,
)
from src.utils import JWTUtils, Security, TokenClaims
from src.utils.auth_service_logger import AuthServiceLogger

from .auth_decorators import is_active_token, is_new_user, is_valid_user
from .auth_service import AuthService


class AuthServiceImpl(AuthService):
    """Implementation of the AuthService for user registration and login."""

    def __init__(
        self,
        auth_repository: IAuthRepository = Depends(AuthRepository),
        session_repository: ISessionRepository = Depends(SessionRepository),
        user_repository: IUserRepository = Depends(UserRepository),
        role_repository: IRoleRepository = Depends(RoleRepository),
        user_role_repository: IUserRoleRepository = Depends(UserRoleRepository),
    ):
        super().__init__(auth_repository)
        self._session_repository = session_repository
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._user_role_repository = user_role_repository
        self._logger = AuthServiceLogger.get_logger()

    @property
    def session_repository(self) -> ISessionRepository:
        return self._session_repository

    @session_repository.setter
    def session_repository(self, session_repository: ISessionRepository) -> None:
        self._session_repository = session_repository

    @property
    def user_repository(self) -> IUserRepository:
        return self._user_repository

    @user_repository.setter
    def user_repository(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    @property
    def role_repository(self) -> IRoleRepository:
        return self._role_repository

    @role_repository.setter
    def role_repository(self, role_repository: IRoleRepository) -> None:
        self._role_repository = role_repository

    @property
    def user_role_repository(self) -> IUserRoleRepository:
        return self._user_role_repository

    @user_role_repository.setter
    def user_role_repository(self, user_role_repository: IUserRoleRepository) -> None:
        self._user_role_repository = user_role_repository

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

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

        role: Role = await self.role_repository.find_by_role_name(db_session, "user")

        if role is None:
            self.logger.error("Failed to create user: role 'user' not found.")
            raise FailToCreateUserException("Failed to create user.")

        await self.auth_repository.save(db_session, user)

        await self.user_role_repository.save(db_session, user_id, role.role_id)

        return user

    @is_valid_user
    async def login(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
        **kwargs,
    ) -> tuple[str, bytes]:
        """Authenticate a user and return a JWT token and user_id."""
        user: User = kwargs["user"]
        user_roles: list[str] = await self.user_repository.find_roles_by_user_id(db_session, user.user_id)

        claims = TokenClaims.for_user(
            user_id=str(UUID(bytes=user.user_id)),
            username=user.username,
            user_roles=user_roles,
        )
        token = JWTUtils.generate_auth_token(claims=claims.to_payload())

        await self.session_repository.save(db_session, token, claims.jti, SessionStatus.ACTIVE, user.user_id)

        return token, user.user_id

    @is_active_token
    async def check_session_status(
        self,
        db_session: AsyncSession,
        token: str,
        user_id: bytes,
        **kwargs,
    ) -> None:
        """Check if the token session is active."""
        self.logger.info(f"Session status check for '{user_id}' is successful.")

    async def get_user_by_id(
        self,
        db_session: AsyncSession,
        user_id: bytes,
    ) -> User:
        """Look up a user by ID. Raises InvalidTokenException if not found."""
        user = await self.user_repository.get_by_id(db_session, user_id)

        if user is None:
            self.logger.info(f"User not found for user_id '{user_id}'.")
            raise InvalidTokenException()

        return user

    async def logout(
        self,
        db_session: AsyncSession,
        token: str,
        user_id: bytes,
    ) -> None:
        """Invalidate a user session."""
        await self.session_repository.update_status(db_session, user_id, token, SessionStatus.INACTIVE)
