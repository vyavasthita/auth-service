"""
Functional tests for POST /login endpoint.

Test data is loaded from ./data/login.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx
import pytest

from src.api.models import User
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "login.json"
BASE_API_URL = "/login"


@pytest.mark.test_section("invalid_request_validation")
@pytest.mark.asyncio
async def test_post_login_invalid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 422 for missing/invalid fields."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        json=namespace_to_dict(test_case.input.body),
    )
    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("valid_request_validation")
@pytest.mark.asyncio
async def test_post_login_valid_request(async_client: httpx.AsyncClient, test_case):
    """Should return 200 with access token on valid credentials."""
    mock_user = MagicMock(spec=User)
    mock_user.username = test_case.mock.user_username
    mock_user.password = test_case.mock.user_password_hash
    mock_user.user_id = UUID(test_case.mock.user_id).bytes

    with (
        patch(
            "src.api.repos.auth_repo.auth_repository.AuthRepository.find_by_username",
            new_callable=AsyncMock,
            return_value=mock_user,
        ),
        patch(
            "src.api.services.auth_service.auth_decorators.Security.verify_password",
            return_value=True,
        ),
        patch(
            "src.api.services.auth_service.auth_service_impl.JWTUtils.generate_auth_token",
            return_value=test_case.mock.token,
        ),
        patch(
            "src.api.repos.session_repo.session_repository.SessionRepository.save",
            new_callable=AsyncMock,
        ),
        patch(
            "src.api.repos.user_repo.user_repository.UserRepository.find_roles_by_user_id",
            new_callable=AsyncMock,
            return_value=["user"],
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

    if hasattr(test_case.output, "cookie"):
        assert test_case.output.cookie in response.cookies


@pytest.mark.test_section("user_not_found_validation")
@pytest.mark.asyncio
async def test_post_login_user_not_found(async_client: httpx.AsyncClient, test_case):
    """Should return 404 when user does not exist."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        json=namespace_to_dict(test_case.input.body),
    )
    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)
