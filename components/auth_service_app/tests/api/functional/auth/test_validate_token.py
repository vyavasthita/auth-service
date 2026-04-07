"""
Functional tests for POST /validate endpoint.

Test data is loaded from ./data/validate_token.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx
import pytest

from src.api import app
from src.api.dependencies.authenticator_dependency import get_authenticator
from src.api.models import SessionStatus, User, UserSession
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "validate_token.json"
BASE_API_URL = "/validate"


@pytest.mark.test_section("valid_token_validation")
@pytest.mark.asyncio
async def test_post_validate_token_valid(async_client: httpx.AsyncClient, test_case):
    """Should return 200 with token validity details."""
    mock_user = MagicMock(spec=User)
    mock_user.user_id = UUID(test_case.mock.user_id).bytes
    mock_user.username = test_case.mock.username

    mock_claims = MagicMock()
    raw_claims = namespace_to_dict(test_case.mock.claims)
    mock_claims.__getitem__ = MagicMock(side_effect=lambda k: raw_claims[k])
    mock_claims.__iter__ = MagicMock(return_value=iter(raw_claims))
    mock_claims.__len__ = MagicMock(return_value=len(raw_claims))
    cookies = namespace_to_dict(test_case.input.cookie)

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.ACTIVE

    mock_authenticator = MagicMock()
    mock_authenticator.validate = AsyncMock(return_value=mock_claims)
    app.dependency_overrides[get_authenticator] = lambda: mock_authenticator

    try:
        with (
            patch(
                "src.api.repos.auth_repo.auth_repository.AuthRepository.find_by_username",
                new_callable=AsyncMock,
                return_value=mock_user,
            ),
            patch(
                "src.api.repos.session_repo.session_repository.SessionRepository.find_by_user_and_token",
                new_callable=AsyncMock,
                return_value=mock_session,
            ),
        ):
            async_client.cookies = cookies
            response = await async_client.post(
                BASE_API_URL,
                headers=namespace_to_dict(test_case.input.headers),
                params={"user_id": test_case.mock.user_id},
            )
    finally:
        async_client.cookies.clear()
        app.dependency_overrides.pop(get_authenticator, None)

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("missing_cookie_validation")
@pytest.mark.asyncio
async def test_post_validate_token_missing_cookie(async_client: httpx.AsyncClient, test_case):
    """Should return 401 when no cookie is provided."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        params={"user_id": test_case.mock.user_id},
    )

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("invalid_token_validation")
@pytest.mark.asyncio
async def test_post_validate_token_invalid(async_client: httpx.AsyncClient, test_case):
    """Should return 401 for invalid/expired tokens."""
    from jwt_lib.exceptions import JWTError

    cookies = namespace_to_dict(test_case.input.cookie)

    mock_authenticator = MagicMock()
    mock_authenticator.validate = AsyncMock(side_effect=JWTError("Invalid token"))
    app.dependency_overrides[get_authenticator] = lambda: mock_authenticator

    try:
        async_client.cookies = cookies
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            params={"user_id": test_case.mock.user_id},
        )
    finally:
        async_client.cookies.clear()
        app.dependency_overrides.pop(get_authenticator, None)

    assert response.status_code == test_case.output.status_code

    assert response.status_code == test_case.output.status_code
