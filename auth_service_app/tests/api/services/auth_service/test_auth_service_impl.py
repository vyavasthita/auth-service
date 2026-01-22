from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions.user_exception import InvalidCredentialsException, UserNotFoundException
from api.models import User
from auth_service_app.api.services import AuthServiceImpl


@pytest.mark.asyncio
async def test_auth_service_impl_import():
    assert AuthServiceImpl is not None


@pytest.mark.asyncio
async def test_login_success_returns_token():
    user = User()
    user.email = "test@example.com"
    user.password = "secret"

    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=user)

    service = AuthServiceImpl(auth_repository=mock_repo)

    token = await service.login(
        MagicMock(spec=AsyncSession),
        email="test@example.com",
        password="secret",
    )

    assert isinstance(token, str)
    assert token
    mock_repo.find_by_email.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_invalid_password_raises():
    user = User()
    user.email = "test@example.com"
    user.password = "secret"

    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=user)

    service = AuthServiceImpl(auth_repository=mock_repo)

    with pytest.raises(InvalidCredentialsException):
        await service.login(
            MagicMock(spec=AsyncSession),
            email="test@example.com",
            password="wrong",
        )


@pytest.mark.asyncio
async def test_login_user_not_found_raises():
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=None)

    service = AuthServiceImpl(auth_repository=mock_repo)

    with pytest.raises(UserNotFoundException):
        await service.login(
            MagicMock(spec=AsyncSession),
            email="missing@example.com",
            password="secret",
        )
