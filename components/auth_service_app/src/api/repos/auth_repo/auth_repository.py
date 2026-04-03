from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos.auth_repo.i_auth_repository import IAuthRepository
from src.api.repos.base import BaseRepository


class AuthRepository(BaseRepository[User, bytes], IAuthRepository):
    """Concrete auth repository — delegates generic CRUD to BaseRepository."""

    def __init__(self):
        super().__init__(User)

    async def save(self, session: AsyncSession, user: User) -> User:
        return await self.create(session, user)

    async def find_by_email(self, session: AsyncSession, email: str) -> User | None:
        try:
            statement = select(User).where(User.email == email).limit(1)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as error:
            self._handle_db_error("find_by_email", error)
