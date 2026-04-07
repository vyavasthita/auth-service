import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.db_exception import DBException, DBIntegrityException, DBOperationalException
from src.utils.auth_service_logger import AuthServiceLogger

from .i_repository import ID, IRepository, T


class BaseRepository(IRepository[T, ID]):
    """Reusable async CRUD — mirrors Spring's SimpleJpaRepository."""

    _logger: logging.Logger = AuthServiceLogger.get_logger()

    def __init__(self, model: type[T]):
        self._model = model

    @property
    def model(self) -> type[T]:
        return self._model

    @model.setter
    def model(self, value: type[T]) -> None:
        self._model = value

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @logger.setter
    def logger(self, value: logging.Logger) -> None:
        self._logger = value

    def _handle_db_error(self, operation: str, error: Exception) -> None:
        entity_name = self._model.__name__

        if isinstance(error, IntegrityError):
            self._logger.error(f"Integrity error during {operation} on {entity_name}: {error}")
            raise DBIntegrityException("Data integrity violation.")

        if isinstance(error, OperationalError):
            self._logger.error(f"Operational error during {operation} on {entity_name}: {error}")
            raise DBOperationalException("Database unavailable.")

        if isinstance(error, SQLAlchemyError):
            self._logger.error(f"Database error during {operation} on {entity_name}: {error}")
            raise DBException("Database error.")

        self._logger.error(f"Unexpected error during {operation} on {entity_name}: {error}")
        raise DBException("Unexpected error.")

    async def get_by_id(self, session: AsyncSession, entity_id: ID) -> T | None:
        try:
            return await session.get(self._model, entity_id)
        except Exception as error:
            self._handle_db_error("get_by_id", error)

    async def get_all(self, session: AsyncSession) -> list[T]:
        try:
            result = await session.execute(select(self._model))
            return list(result.scalars().all())
        except Exception as error:
            self._handle_db_error("get_all", error)

    async def create(self, session: AsyncSession, entity: T) -> T:
        try:
            session.add(entity)
            await session.flush()
            return entity
        except Exception as error:
            self._handle_db_error("create", error)

    async def update(self, session: AsyncSession, entity: T) -> T:
        try:
            merged = await session.merge(entity)
            await session.flush()
            return merged
        except Exception as error:
            self._handle_db_error("update", error)

    async def delete(self, session: AsyncSession, entity_id: ID) -> None:
        try:
            entity = await self.get_by_id(session, entity_id)
            if entity:
                await session.delete(entity)
                await session.flush()
        except (DBException, DBIntegrityException, DBOperationalException):
            raise
        except Exception as error:
            self._handle_db_error("delete", error)
