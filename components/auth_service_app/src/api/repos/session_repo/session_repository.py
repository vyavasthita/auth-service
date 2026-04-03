from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import SessionStatus, UserSession
from src.api.repos.base import BaseRepository
from src.api.repos.session_repo.i_session_repository import ISessionRepository


class SessionRepository(BaseRepository[UserSession, bytes], ISessionRepository):
    """Concrete session repository — delegates generic CRUD to BaseRepository."""

    def __init__(self):
        super().__init__(UserSession)

    async def save(self, session: AsyncSession, token: str, status: SessionStatus, user_id: bytes) -> UserSession:
        user_session = UserSession(
            user_session_id=uuid4().bytes,
            token=token,
            status=status,
            user_id=user_id,
        )
        return await self.create(session, user_session)

    async def find_by_user_and_token(self, session: AsyncSession, user_id: bytes, token: str) -> UserSession | None:
        try:
            statement = (
                select(UserSession).where(UserSession.user_id == user_id).where(UserSession.token == token).limit(1)
            )
            result = await session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as error:
            self._handle_db_error("find_by_user_and_token", error)
