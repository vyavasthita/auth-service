import pytest
from src.api.services import AuthService

@pytest.mark.asyncio
async def test_auth_service_import():
    assert AuthService is not None
