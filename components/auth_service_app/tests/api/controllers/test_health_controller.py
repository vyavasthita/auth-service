import pytest
from src.api.controllers import HealthController


@pytest.mark.asyncio
async def test_health_controller_import():
    assert HealthController() is not None