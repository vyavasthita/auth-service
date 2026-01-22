import pytest
from auth_service_app.api.repositories import AuthRepositoryImpl

@pytest.mark.asyncio
async def test_auth_repository_impl_import():
    assert AuthRepositoryImpl is not None