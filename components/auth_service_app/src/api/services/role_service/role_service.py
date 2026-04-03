from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User
from src.api.repos import IRoleRepository
from src.utils import AuthServiceLogger


class RoleService(ABC):
    """Abstract base class for role service."""

    def __init__(self, role_repository: IRoleRepository):
        self._logger = AuthServiceLogger.get_logger()
        self._role_repository = role_repository

    @property
    def logger(self) -> AuthServiceLogger:
        return self._logger
    
    @logger.setter
    def logger(self, logger: AuthServiceLogger) -> None:
        self._logger = logger

    @property
    def role_repository(self) -> IRoleRepository:
        return self._role_repository
    
    @role_repository.setter
    def role_repository(self, role_repository: IRoleRepository) -> None:
        self._role_repository = role_repository

    @property
    def role_repository(self) -> IRoleRepository:
        return self._role_repository

    @role_repository.setter
    def role_repository(self, role_repository: IRoleRepository) -> None:
        self._role_repository = role_repository

    async def _check_role(self, db_session: AsyncSession, role: str) -> User | None:
        return await self.role_repository.find_by_role(db_session, role=role)
