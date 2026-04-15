"""Unit tests for the is_active_token decorator (session check only)."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.exceptions import InvalidTokenException
from src.api.models import SessionStatus, UserSession


class FakeService:
    """Minimal stand-in for AuthServiceImpl to test decorators in isolation."""

    def __init__(self, session_return=None):
        self.session_repository = MagicMock()
        self.session_repository.find_by_user_and_token = AsyncMock(return_value=session_return)
        self.logger = MagicMock()


@pytest.mark.asyncio
async def test_is_active_token_passes_with_active_session():
    """is_active_token allows through when session is active."""
    from src.api.services.auth_service.auth_decorators import is_active_token

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.ACTIVE

    svc = FakeService(session_return=mock_session)

    called = False

    @is_active_token
    async def target(self, db_session, token, user_id, **kwargs):
        nonlocal called
        called = True

    await target(svc, MagicMock(), "some.jwt.token", b"\x01" * 16)
    assert called


@pytest.mark.asyncio
async def test_is_active_token_raises_on_inactive_session():
    """is_active_token raises InvalidTokenException when session is inactive."""
    from src.api.services.auth_service.auth_decorators import is_active_token

    mock_session = MagicMock(spec=UserSession)
    mock_session.status = SessionStatus.INACTIVE

    svc = FakeService(session_return=mock_session)

    @is_active_token
    async def target(self, db_session, token, user_id, **kwargs):
        pass

    with pytest.raises(InvalidTokenException):
        await target(svc, MagicMock(), "some.jwt.token", b"\x01" * 16)


@pytest.mark.asyncio
async def test_is_active_token_raises_on_missing_session():
    """is_active_token raises InvalidTokenException when no session found."""
    from src.api.services.auth_service.auth_decorators import is_active_token

    svc = FakeService(session_return=None)

    @is_active_token
    async def target(self, db_session, token, user_id, **kwargs):
        pass

    with pytest.raises(InvalidTokenException):
        await target(svc, MagicMock(), "some.jwt.token", b"\x01" * 16)
