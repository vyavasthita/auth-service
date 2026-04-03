import pytest
from src.api.controllers import health_router


@pytest.mark.asyncio
async def test_health_controller_import():
    assert health_router is not None