from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.api.repos import DatabaseEngine
from src.utils import AuthServiceLogger
from src.api.exceptions import DBException
from src.api.dependencies.config_dependency import Config


logger = AuthServiceLogger.get_logger()

_engine = DatabaseEngine().get_engine()
_session_local = async_sessionmaker(bind=_engine, expire_on_commit=False)


class DatabaseDependency:
    @staticmethod
    async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with _session_local() as db:
            logger.debug(f"DB session created: {id(db)}")
            try:
                yield db
                await db.commit()
            except Exception:
                await db.rollback()
                raise
            finally:
                logger.debug(f"DB session closed: {id(db)}")
                await db.close()

    async def check_connectivity(self, db: AsyncSession) -> None:
        try:
            statement = text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = :schema"
            )
            result = await db.execute(statement, {"schema": Config().MYSQL_DATABASE})
            records = result.all()
            logger.debug(f"Tables: {[record[0] for record in records]}")
        except Exception as error:
            logger.error(f"Failed DB check: {error}")
            raise DBException(
                message="Internal Server Error",
            )

    async def __call__(self) -> None:
        logger.info("Validating database connectivity...")
        async with _session_local() as db:
            await self.check_connectivity(db)
