from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(ABC, Generic[T, ID]):
    """Generic repository interface — mirrors JPA's JpaRepository<T, ID>."""

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, entity_id: ID) -> Optional[T]:
        raise NotImplementedError("Subclasses must implement 'get_by_id'.")

    @abstractmethod
    async def get_all(self, session: AsyncSession) -> List[T]:
        raise NotImplementedError("Subclasses must implement 'get_all'.")

    @abstractmethod
    async def create(self, session: AsyncSession, entity: T) -> T:
        raise NotImplementedError("Subclasses must implement 'create'.")

    @abstractmethod
    async def update(self, session: AsyncSession, entity: T) -> T:
        raise NotImplementedError("Subclasses must implement 'update'.")

    @abstractmethod
    async def delete(self, session: AsyncSession, entity_id: ID) -> None:
        raise NotImplementedError("Subclasses must implement 'delete'.")
