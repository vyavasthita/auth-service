"""
Functional tests for POST /register endpoint.

Test data is loaded from ./data/register.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx
import pytest

from src.api.models import Role
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "register.json"
BASE_API_URL = "/register"


@pytest.mark.test_section("invalid_request_validation")
@pytest.mark.asyncio
async def test_post_register_invalid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 422 for missing/invalid fields."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        json=namespace_to_dict(test_case.input.body),
    )
    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("valid_request_validation")
@pytest.mark.asyncio
async def test_post_register_valid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 201 with registered user details."""
    mock_user_uuid = UUID(test_case.mock.uuid)

    mock_role = MagicMock(spec=Role)
    mock_role.role_id = b"\x01" * 16
    mock_role.role_name = "user"

    with (
        patch(
            "src.api.services.auth_service.auth_service_impl.uuid4",
            return_value=mock_user_uuid,
        ),
        patch(
            "src.api.services.auth_service.auth_service_impl.Security.hash_password",
            return_value="$2b$12$mockedhashvalue",
        ),
        patch(
            "src.api.repos.role_repo.role_repository.RoleRepository.find_by_role_name",
            new_callable=AsyncMock,
            return_value=mock_role,
        ),
        patch(
            "src.api.repos.user_role_repo.user_role_repository.UserRoleRepository.save",
            new_callable=AsyncMock,
            return_value=MagicMock(),
        ),
    ):
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            json=namespace_to_dict(test_case.input.body),
        )

    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)
