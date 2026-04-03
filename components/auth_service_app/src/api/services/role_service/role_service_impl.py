from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Role
from src.api.repos import IRoleRepository, RoleRepository

from .role_decorators import is_new_role
from .role_service import RoleService


class RoleServiceImpl(RoleService):
    """Implementation of the RoleService for role management."""

    def __init__(
        self,
        role_repository: IRoleRepository = Depends(RoleRepository),
    ):
        super().__init__(role_repository)

    @is_new_role
    async def add_role(
        self,
        db_session: AsyncSession,
        role_name: str,
    ) -> Role:
        """Register a new role."""
        return await self.role_repository.save(db_session, role_name)
