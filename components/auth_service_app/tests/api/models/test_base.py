import pytest
from src.api.models import Base

@pytest.mark.asyncio
async def test_base_model_import():
    assert Base is not None
