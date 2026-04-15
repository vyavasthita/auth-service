"""
Functional tests for GET /users/me endpoint.

Test data is loaded from ./data/get_me.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx
import pytest

from src.api.models import SessionStatus, User, UserSession
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "get_me.json"
BASE_API_URL = "/users/me"


@pytest.mark.test_section("valid_token_validation")
@pytest.mark.asyncio
async def test_get_me_valid(async_client: httpx.AsyncClient, test_case):
    """Should return 200 with user details for a valid token."""
    mock_user = MagicMock(spec=User)
    mock_user.user_id = UUID(test_case.mock.user_id).bytes
    mock_user.username = test_case.mock.username
    mock_user.created_at = datetime.fromisoformat(test_case.mock.created_at)

    cookies = namespace_to_dict(test_case.input.cookie)

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.ACTIVE

    with (
        patch(
            "src.api.repos.session_repo.session_repository.SessionRepository.find_by_user_and_token",
            new_callable=AsyncMock,
            return_value=mock_session,
        ),
        patch(
            "src.api.repos.user_repo.user_repository.UserRepository.get_by_id",
            new_callable=AsyncMock,
            return_value=mock_user,
        ),
    ):
        async_client.cookies = cookies
        response = await async_client.get(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            params={"user_id": test_case.mock.user_id},
        )

    async_client.cookies.clear()

    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)


@pytest.mark.test_section("missing_cookie_validation")
@pytest.mark.asyncio
async def test_get_me_missing_cookie(async_client: httpx.AsyncClient, test_case):
    """Should return 401 when no cookie is provided."""
    response = await async_client.get(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        params={"user_id": test_case.mock.user_id},
    )

    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)


@pytest.mark.test_section("inactive_session")
@pytest.mark.asyncio
async def test_get_me_inactive_session(async_client: httpx.AsyncClient, test_case):
    """Should return 401 when the session is inactive."""
    cookies = namespace_to_dict(test_case.input.cookie)

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.INACTIVE

    with patch(
        "src.api.repos.session_repo.session_repository.SessionRepository.find_by_user_and_token",
        new_callable=AsyncMock,
        return_value=mock_session,
    ):
        async_client.cookies = cookies
        response = await async_client.get(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            params={"user_id": test_case.mock.user_id},
        )

    async_client.cookies.clear()

    assert response.status_code == test_case.output.status_code

    if hasattr(test_case.output, "body"):
        assert response.json() == namespace_to_dict(test_case.output.body)
