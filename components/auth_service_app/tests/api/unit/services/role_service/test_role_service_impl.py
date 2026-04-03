from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import RoleAlreadyExistsException
from src.api.models import Role
from src.api.services import RoleServiceImpl


@pytest.mark.asyncio
async def test_role_service_impl_import():
    assert RoleServiceImpl is not None


@pytest.mark.asyncio
async def test_add_role_success():
    mock_role = MagicMock(spec=Role)
    mock_role.role_name = "admin"

    mock_repo = MagicMock()
    mock_repo.find_by_role_name = AsyncMock(return_value=None)
    mock_repo.save = AsyncMock(return_value=mock_role)

    service = RoleServiceImpl(role_repository=mock_repo)

    result = await service.add_role(
        MagicMock(spec=AsyncSession),
        "admin",
    )

    assert result.role_name == "admin"
    mock_repo.find_by_role_name.assert_awaited_once()
    mock_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_role_already_exists_raises():
    existing_role = MagicMock(spec=Role)
    existing_role.role_name = "admin"

    mock_repo = MagicMock()
    mock_repo.find_by_role_name = AsyncMock(return_value=existing_role)

    service = RoleServiceImpl(role_repository=mock_repo)

    with pytest.raises(RoleAlreadyExistsException):
        await service.add_role(
            MagicMock(spec=AsyncSession),
            "admin",
        )
