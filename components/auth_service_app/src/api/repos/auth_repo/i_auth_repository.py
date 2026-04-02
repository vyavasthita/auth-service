from abc import abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos.base import IRepository


class IAuthRepository(IRepository[User, bytes]):
    """Abstract interface for auth-specific repository operations."""

    @abstractmethod
    async def find_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        raise NotImplementedError("Subclasses must implement 'find_by_email'.")
