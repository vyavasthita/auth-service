import logging
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from fastapi import status
from api.models import User
from .auth_repository import AuthRepository
from api.exceptions import DBConnectionException

class AuthRepositoryImpl(AuthRepository):
    """
    For all CRUD operations in DB for User object.
    """
    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    async def save(self, db_session: AsyncSession, user: User) -> User:
        # Stage the user object for insertion into the database
        db_session.add(user)
        
        # Commit the transaction to persist the user
        await db_session.commit()
        
        # Refresh the user object with any DB-generated fields (e.g., auto-incremented id)
        await db_session.refresh(user)
        
        # Return the persisted user object
        return user
    

    async def find_by_id(self, db_session: AsyncSession, user_id: UUID) -> Optional[User]:
        # Build a select statement to find a user by id
        try:
            statement = select(User).where(User.id == user_id.bytes).limit(1)
            result = await db_session.execute(statement)
            return result.scalar_one_or_none()
        except OperationalError as error:
            self._logger.error(f"Operational error while finding user by id: {error}")
            raise DBConnectionException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Operational error while processing your request.",
            )
        except SQLAlchemyError as error:
            self._logger.error(f"Database error while finding user by id: {error}")
            raise DBConnectionException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Database error while processing your request.",
            )

    async def find_by_email(self, db_session: AsyncSession, email: str) -> Optional[User]:
        # Build a select statement to find a user by email
        try:
            statement = select(User).where(User.email == email).limit(1)
            result = await db_session.execute(statement)
            return result.scalar_one_or_none()
        except OperationalError as error:
            self._logger.error(f"Operational error while checking packages: {error}")
            raise DBConnectionException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Operational error while processing your request.",
            )
        except SQLAlchemyError as error:
            self._logger.error(f"Database error while checking packages: {error}")
            raise DBConnectionException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Database error while processing your request.",
            )