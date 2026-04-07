from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos.base import IRepository


class IAuthRepository(IRepository[User, bytes]):
    """Abstract interface for auth-specific repository operations."""

    @abstractmethod
    async def save(self, session: AsyncSession, user: User) -> User:
        raise NotImplementedError("Subclasses must implement 'save'.")

    @abstractmethod
    async def find_by_username(self, session: AsyncSession, username: str) -> User | None:
        raise NotImplementedError("Subclasses must implement 'find_by_username'.")
