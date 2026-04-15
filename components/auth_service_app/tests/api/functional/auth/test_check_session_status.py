"""
Functional tests for POST /session-status endpoint.

Test data is loaded from ./data/check_session_status.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.api.models import SessionStatus, UserSession
from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "check_session_status.json"
BASE_API_URL = "/session-status"


@pytest.mark.test_section("active_session")
@pytest.mark.asyncio
async def test_post_check_session_status_active(async_client: httpx.AsyncClient, test_case):
    """Should return 200 when the session is active."""
    cookies = namespace_to_dict(test_case.input.cookie)

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.ACTIVE

    with patch(
        "src.api.repos.session_repo.session_repository.SessionRepository.find_by_user_and_token",
        new_callable=AsyncMock,
        return_value=mock_session,
    ):
        async_client.cookies = cookies
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            params={"user_id": test_case.mock.user_id},
        )

    async_client.cookies.clear()

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("missing_cookie")
@pytest.mark.asyncio
async def test_post_check_session_status_missing_cookie(async_client: httpx.AsyncClient, test_case):
    """Should return 422 when no cookie is provided."""
    response = await async_client.post(
        BASE_API_URL,
        headers=namespace_to_dict(test_case.input.headers),
        params={"user_id": test_case.mock.user_id},
    )

    assert response.status_code == test_case.output.status_code


@pytest.mark.test_section("inactive_session")
@pytest.mark.asyncio
async def test_post_check_session_status_inactive(async_client: httpx.AsyncClient, test_case):
    """Should return 401 when the session is inactive or missing."""
    cookies = namespace_to_dict(test_case.input.cookie)

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.INACTIVE

    with patch(
        "src.api.repos.session_repo.session_repository.SessionRepository.find_by_user_and_token",
        new_callable=AsyncMock,
        return_value=mock_session,
    ):
        async_client.cookies = cookies
        response = await async_client.post(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
            params={"user_id": test_case.mock.user_id},
        )

    async_client.cookies.clear()

    assert response.status_code == test_case.output.status_code
