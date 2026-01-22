from typing import Optional
from uuid import UUID
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import User


class AuthRepository(ABC):
    """For all CRUD operations in DB for User object."""

    @abstractmethod
    async def save(self, db_session: AsyncSession, user: User) -> User:
        raise NotImplementedError("Method 'save' needs implementation.")

    @abstractmethod
    async def find_by_id(self, db_session: AsyncSession, user_id: UUID) -> Optional[User]:
        raise NotImplementedError("Method 'find_by_id' needs implementation.")

    @abstractmethod
    async def find_by_email(self, db_session: AsyncSession, email: str) -> Optional[User]:
        raise NotImplementedError("Method 'find_by_email' needs implementation.")