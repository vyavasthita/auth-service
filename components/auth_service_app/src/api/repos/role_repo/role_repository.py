from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Role
from src.api.repos.base import BaseRepository
from .i_role_repository import IRoleRepository


class RoleRepository(BaseRepository[Role, bytes], IRoleRepository):
    """Concrete role repository — delegates generic CRUD to BaseRepository."""

    def __init__(self):
        super().__init__(Role)

    async def save(self, session: AsyncSession, role_name: str) -> Role:
        return await self.create(session, Role(role_name=role_name))

    async def find_by_role_name(self, session: AsyncSession, role_name: str) -> Role | None:
        try:
            statement = select(Role).where(Role.role_name == role_name).limit(1)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as error:
            self._handle_db_error("find_by_role_name", error)
