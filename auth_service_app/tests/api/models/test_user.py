import pytest
from api.models import User

@pytest.mark.asyncio
async def test_user_model_import():
    assert User is not None
