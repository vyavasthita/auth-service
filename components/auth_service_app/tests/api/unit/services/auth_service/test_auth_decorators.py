"""Unit tests for the is_valid_token decorator (token-validator integration)."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.exceptions import InvalidTokenException, UserNotFoundException
from src.api.models import User


class FakeService:
    """Minimal stand-in for AuthServiceImpl to test decorators in isolation."""

    def __init__(self, authenticator, check_user_return=None):
        self._authenticator = authenticator
        self._check_user_result = check_user_return
        self.logger = MagicMock()

    async def _check_user(self, db_session, username):
        return self._check_user_result


@pytest.mark.asyncio
async def test_is_valid_token_calls_authenticator_validate():
    """is_valid_token delegates to self._authenticator.validate."""
    from src.api.services.auth_service.auth_decorators import is_valid_token

    mock_authenticator = MagicMock()
    mock_claims = MagicMock()
    mock_claims.__getitem__ = MagicMock(side_effect=lambda k: {"sub": "user-uuid-1", "username": "testuser"}[k])
    mock_authenticator.validate = AsyncMock(return_value=mock_claims)

    user = MagicMock(spec=User)
    user.username = "testuser"

    svc = FakeService(authenticator=mock_authenticator, check_user_return=user)

    @is_valid_token
    async def target(self, db_session, token, user_id, **kwargs):
        return kwargs.get("user")

    result = await target(svc, MagicMock(), "some.jwt.token", b"\x01" * 16)

    mock_authenticator.validate.assert_awaited_once_with("some.jwt.token")
    assert result is user


@pytest.mark.asyncio
async def test_is_valid_token_raises_on_jwt_error():
    """is_valid_token raises InvalidTokenException when authenticator raises JWTError."""
    from jwt_lib.exceptions import JWTError

    from src.api.services.auth_service.auth_decorators import is_valid_token

    mock_authenticator = MagicMock()
    mock_authenticator.validate = AsyncMock(side_effect=JWTError("bad token"))

    svc = FakeService(authenticator=mock_authenticator)

    @is_valid_token
    async def target(self, db_session, token, user_id, **kwargs):
        return kwargs.get("user")

    with pytest.raises(InvalidTokenException):
        await target(svc, MagicMock(), "bad.jwt.token", b"\x01" * 16)


@pytest.mark.asyncio
async def test_is_valid_token_raises_when_user_not_found():
    """is_valid_token raises UserNotFoundException when sub doesn't match a user."""
    from src.api.services.auth_service.auth_decorators import is_valid_token

    mock_authenticator = MagicMock()
    mock_claims = MagicMock()
    mock_claims.__getitem__ = MagicMock(side_effect=lambda k: {"sub": "user-uuid-2", "username": "ghost"}[k])
    mock_authenticator.validate = AsyncMock(return_value=mock_claims)

    svc = FakeService(authenticator=mock_authenticator, check_user_return=None)

    @is_valid_token
    async def target(self, db_session, token, user_id, **kwargs):
        return kwargs.get("user")

    with pytest.raises(UserNotFoundException):
        await target(svc, MagicMock(), "valid.jwt.token", b"\x01" * 16)


@pytest.mark.asyncio
async def test_is_valid_token_passes_user_in_kwargs():
    """is_valid_token injects the looked-up user into kwargs."""
    from src.api.services.auth_service.auth_decorators import is_valid_token

    mock_authenticator = MagicMock()
    mock_claims = MagicMock()
    mock_claims.__getitem__ = MagicMock(side_effect=lambda k: {"sub": "user-uuid-3", "username": "alice"}[k])
    mock_claims.__iter__ = MagicMock(return_value=iter({"sub": "user-uuid-3", "username": "alice"}))
    mock_authenticator.validate = AsyncMock(return_value=mock_claims)

    user = MagicMock(spec=User)
    user.username = "alice"

    svc = FakeService(authenticator=mock_authenticator, check_user_return=user)

    captured_kwargs = {}

    @is_valid_token
    async def target(self, db_session, token, user_id, **kwargs):
        captured_kwargs.update(kwargs)
        return kwargs.get("user")

    await target(svc, MagicMock(), "good.jwt.token", b"\x01" * 16)
    assert captured_kwargs["user"] is user
