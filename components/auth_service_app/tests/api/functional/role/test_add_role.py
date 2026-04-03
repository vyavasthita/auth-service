"""
Functional tests for POST /roles endpoint.

Test data is loaded from ./data/add_role.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.api.models import Role
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "add_role.json"
BASE_API_URL = "/roles"


@pytest.mark.test_section("invalid_request_validation")
@pytest.mark.asyncio
async def test_post_add_role_invalid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 422 for missing/invalid fields."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        json=namespace_to_dict(test_case.input.body),
    )
    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("valid_request_validation")
@pytest.mark.asyncio
async def test_post_add_role_valid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 201 with success message."""
    mock_role = MagicMock(spec=Role)
    mock_role.role_name = test_case.mock.role_name

    with (
        patch(
            "src.api.repos.role_repo.role_repository.RoleRepository.find_by_role_name",
            new_callable=AsyncMock,
            return_value=None,
        ),
        patch(
            "src.api.repos.role_repo.role_repository.RoleRepository.save",
            new_callable=AsyncMock,
            return_value=mock_role,
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


@pytest.mark.test_section("role_already_exists_validation")
@pytest.mark.asyncio
async def test_post_add_role_already_exists(async_client: httpx.AsyncClient, test_case):
    """Should return 409 when role already exists."""
    existing_role = MagicMock(spec=Role)
    existing_role.role_name = test_case.mock.role_name

    with patch(
        "src.api.repos.role_repo.role_repository.RoleRepository.find_by_role_name",
        new_callable=AsyncMock,
        return_value=existing_role,
    ):
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            json=namespace_to_dict(test_case.input.body),
        )

    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)
