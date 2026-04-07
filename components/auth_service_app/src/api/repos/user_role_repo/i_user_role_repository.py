from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import UserRole
from src.api.repos.base import IRepository


class IUserRoleRepository(IRepository[UserRole, bytes]):
    """Abstract interface for user-role-specific repository operations."""

    async def save(self, session: AsyncSession, user_id: bytes, role_id: bytes) -> UserRole:
        raise NotImplementedError("Subclasses must implement 'save'.")
