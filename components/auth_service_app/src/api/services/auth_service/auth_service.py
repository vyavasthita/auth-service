from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos import IAuthRepository
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

    async def _check_user(self, db_session: AsyncSession, username: str) -> User | None:
        return await self.auth_repository.find_by_username(db_session, username=username)

    @abstractmethod
    async def register(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
    ) -> User:
        raise NotImplementedError("Method 'register' needs implementation.")

    @abstractmethod
    async def login(
        self,
        db_session: AsyncSession,
        username: str,
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
