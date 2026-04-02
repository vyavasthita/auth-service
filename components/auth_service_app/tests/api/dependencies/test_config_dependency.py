import pytest
from src.api.dependencies import Config


@pytest.mark.asyncio
async def test_get_config_import():
    assert Config() is not None