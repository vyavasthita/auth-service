from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import DatabaseDependency
from src.api.dependencies.config_dependency import Config
from src.api.dtos import (
    AddRoleRequestDTO,
    AddRoleResponseDTO,
)
from src.api.services import RoleService, RoleServiceImpl
from src.utils import AuthServiceLogger

logger = AuthServiceLogger.get_logger()


config = Config()


role_router = APIRouter(
    prefix="/roles",
    tags=["Role"],
)


@role_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def add_role(
    request: AddRoleRequestDTO,
    role_service: RoleService = Depends(RoleServiceImpl),
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
) -> AddRoleResponseDTO:
    """Register a new role."""
    role = await role_service.add_role(db_session, request.role_name)
    return AddRoleResponseDTO(message=f"Role '{role.role_name}' added successfully.")
