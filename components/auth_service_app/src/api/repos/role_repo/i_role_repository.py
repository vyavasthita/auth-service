from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Role
from src.api.repos.base import IRepository


class IRoleRepository(IRepository[Role, bytes]):
    """Abstract interface for role-specific repository operations."""

    async def save(
        self, session: AsyncSession, role_name: str) -> Role:
        raise NotImplementedError("Subclasses must implement 'save'.")

    @abstractmethod
    async def find_by_role_name(self, session: AsyncSession, role_name: str) -> Role | None:
        raise NotImplementedError("Subclasses must implement 'find_by_role_name'.")
