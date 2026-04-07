from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Role, User, UserRole
from src.api.repos.base import BaseRepository

from .i_user_repository import IUserRepository


class UserRepository(BaseRepository[User, bytes], IUserRepository):
    """Concrete user repository — delegates generic CRUD to BaseRepository."""

    def __init__(self):
        super().__init__(User)

    async def save(self, session: AsyncSession, username: str, password: str) -> User:
        user = User(
            user_id=uuid4().bytes,
            username=username,
            password=password,
        )
        return await self.create(session, user)

    async def find_roles_by_user_id(self, session: AsyncSession, user_id: bytes) -> list[str] | None:
        try:
            result = await session.execute(
                select(Role.role_name)
                .join(UserRole, UserRole.role_id == Role.role_id)
                .where(UserRole.user_id == user_id)
            )
            roles = list(result.scalars().all())
            return roles if roles else None
        except Exception as error:
            self._handle_db_error("find_roles_by_user_id", error)
