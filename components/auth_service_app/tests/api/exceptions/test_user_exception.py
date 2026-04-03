import pytest

from src.api.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


@pytest.mark.asyncio
async def test_user_already_exists_exception():
    exc = UserAlreadyExistsException("exists")
    assert "already exists" in str(exc)
    assert exc.status_code == 409


@pytest.mark.asyncio
async def test_user_not_found_exception():
    exc = UserNotFoundException("missing")
    assert "missing" in str(exc)
    assert exc.status_code == 404


@pytest.mark.asyncio
async def test_invalid_credentials_exception():
    exc = InvalidCredentialsException()
    assert str(exc) == "Invalid email or password."
    assert exc.status_code == 401
