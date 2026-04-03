from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import SessionStatus, UserSession
from src.api.repos.base import IRepository


class ISessionRepository(IRepository[UserSession, bytes]):
    """Abstract interface for session-specific repository operations."""

    async def save(self, session: AsyncSession, token: str, status: SessionStatus, user_id: bytes) -> UserSession:
        raise NotImplementedError("Subclasses must implement 'save'.")

    @abstractmethod
    async def find_by_user_and_token(self, session: AsyncSession, user_id: bytes, token: str) -> UserSession | None:
        raise NotImplementedError("Subclasses must implement 'find_by_user_and_token'.")
