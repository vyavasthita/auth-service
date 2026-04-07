from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import UserRole
from src.api.repos.base import BaseRepository

from .i_user_role_repository import IUserRoleRepository


class UserRoleRepository(BaseRepository[UserRole, bytes], IUserRoleRepository):
    """Concrete user-role repository — delegates generic CRUD to BaseRepository."""

    def __init__(self):
        super().__init__(UserRole)

    async def save(self, session: AsyncSession, user_id: bytes, role_id: bytes) -> UserRole:
        user_role = UserRole(
            user_role_id=uuid4().bytes,
            user_id=user_id,
            role_id=role_id,
        )
        return await self.create(session, user_role)
