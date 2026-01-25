from typing import AsyncGenerator
import logging
from fastapi import status, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from api.repositories import BaseDB
from api.exceptions import DBConnectionException
from api.dependencies import Config


# Async engine from BaseDB (ensure BaseDB uses create_async_engine)
_engine = BaseDB().get_engine()
_session_local = async_sessionmaker(bind=_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a SQLAlchemy AsyncSession for database operations.

    Yields:
        AsyncSession: The database session.
    """
    logger = logging.getLogger(__name__)
    
    async with _session_local() as db:
        logger.debug(f"DB session created: {id(db)}")
        try:
            yield db
        finally:
            logger.debug(f"DB session closed: {id(db)}")
            await db.close()


class ValidateDBConnection:
    logger = logging.getLogger(__name__)

    async def _validate(self, db: AsyncSession) -> None:
        """
        Validates the database connection by executing a test query.

        Args:
            db (AsyncSession): The database session to validate.

        Raises:
            DBConnectionException: If the database check fails.
        """
        try:
            statement = text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = :schema"
            )
            result = await db.execute(statement, {"schema": Config().MYSQL_DATABASE})
            records = result.all()
            self.logger.debug(f"Tables: {[record[0] for record in records]}")
        except Exception as error:
            self.logger.error(f"Failed DB check: {error}")
            raise DBConnectionException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
            )

    async def __call__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        """
        Callable dependency to validate database connectivity for FastAPI routes.

        Args:
            db (AsyncSession): The database session dependency.
        """
        self.logger.info("Database connectivity validated.")
        await self._validate(db)
