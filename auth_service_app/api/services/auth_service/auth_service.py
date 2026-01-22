from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import User
from api.repositories import AuthRepository


class AuthService(ABC):
    def __init__(self, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    @property
    def auth_repository(self) -> AuthRepository:
        return self._auth_repository

    @auth_repository.setter
    def auth_repository(self, auth_repository: AuthRepository) -> None:
        self._auth_repository = auth_repository

    @abstractmethod
    async def register(
        self,
        db_session: AsyncSession,
        name: str,
        email: str,
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