"""
Functional tests for POST /validate endpoint.

Test data is loaded from ./data/validate_token.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import jwt
import pytest

from src.api.models import User
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "validate_token.json"
BASE_API_URL = "/validate"


@pytest.mark.test_section("valid_token_validation")
@pytest.mark.asyncio
async def test_post_validate_token_valid(async_client: httpx.AsyncClient, test_case):
    """Should return 200 with token validity details."""
    mock_user = MagicMock(spec=User)
    mock_user.user_id = test_case.mock.user_id
    mock_user.email = test_case.mock.email

    mock_claims = namespace_to_dict(test_case.mock.claims)
    cookies = namespace_to_dict(test_case.input.cookie)

    with (
        patch(
            "src.api.services.auth_service.auth_decorators.JWTUtils.decode_auth_token",
            return_value=mock_claims,
        ),
        patch(
            "src.api.repos.auth_repo.auth_repository.AuthRepository.find_by_email",
            new_callable=AsyncMock,
            return_value=mock_user,
        ),
    ):
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            cookies=cookies,
        )

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("missing_cookie_validation")
@pytest.mark.asyncio
async def test_post_validate_token_missing_cookie(async_client: httpx.AsyncClient, test_case):
    """Should return 401 when no cookie is provided."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
    )

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("invalid_token_validation")
@pytest.mark.asyncio
async def test_post_validate_token_invalid(async_client: httpx.AsyncClient, test_case):
    """Should return 401 for invalid/expired tokens."""
    cookies = namespace_to_dict(test_case.input.cookie)

    with patch(
        "src.api.services.auth_service.auth_decorators.JWTUtils.decode_auth_token",
        side_effect=jwt.InvalidTokenError("Invalid token"),
    ):
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            cookies=cookies,
        )

    assert response.status_code == test_case.output.status_code
