from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos.base import IRepository


class IUserRepository(IRepository[User, bytes]):
    """Abstract interface for user-specific repository operations."""

    async def save(self, session: AsyncSession, username: str, password: str) -> User:
        raise NotImplementedError("Subclasses must implement 'save'.")

    @abstractmethod
    async def find_roles_by_user_id(self, session: AsyncSession, user_id: bytes) -> list[str] | None:
        raise NotImplementedError("Subclasses must implement 'find_roles_by_user_id'.")
