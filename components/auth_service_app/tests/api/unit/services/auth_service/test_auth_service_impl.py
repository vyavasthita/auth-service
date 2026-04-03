from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.user_exception import InvalidCredentialsException, UserNotFoundException
from src.api.models import User
from src.api.services import AuthServiceImpl
from src.utils.security import Security


@pytest.mark.asyncio
async def test_auth_service_impl_import():
    assert AuthServiceImpl is not None


@pytest.mark.asyncio
async def test_login_success_returns_token():
    user = User()
    user.username = "testuser"
    # Use a valid bcrypt hash for the password
    user.password = Security.hash_password("secret")

    mock_repo = MagicMock()
    mock_repo.find_by_username = AsyncMock(return_value=user)

    mock_session_repo = MagicMock()
    mock_session_repo.save = AsyncMock()

    service = AuthServiceImpl(auth_repository=mock_repo, session_repository=mock_session_repo)

    token = await service.login(
        MagicMock(spec=AsyncSession),
        username="testuser",
        password="secret",
    )

    assert isinstance(token, str)
    assert token
    mock_repo.find_by_username.assert_awaited_once()
    mock_session_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_invalid_password_raises():
    user = User()
    user.username = "testuser"
    # Use a valid bcrypt hash for the password
    user.password = Security.hash_password("secret")

    mock_repo = MagicMock()
    mock_repo.find_by_username = AsyncMock(return_value=user)

    service = AuthServiceImpl(auth_repository=mock_repo, session_repository=MagicMock())

    with pytest.raises(InvalidCredentialsException):
        await service.login(
            MagicMock(spec=AsyncSession),
            username="testuser",
            password="wrong",
        )


@pytest.mark.asyncio
async def test_login_user_not_found_raises():
    mock_repo = MagicMock()
    mock_repo.find_by_username = AsyncMock(return_value=None)

    service = AuthServiceImpl(auth_repository=mock_repo, session_repository=MagicMock())

    with pytest.raises(UserNotFoundException):
        await service.login(
            MagicMock(spec=AsyncSession),
            username="missing_user",
            password="secret",
        )
