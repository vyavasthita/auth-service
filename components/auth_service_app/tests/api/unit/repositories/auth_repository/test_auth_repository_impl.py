import pytest

from src.api.repos import AuthRepository


@pytest.mark.asyncio
async def test_auth_repository_impl_import():
    assert AuthRepository is not None
