import pytest

from src.api.models import User, UserProfile


@pytest.mark.asyncio
async def test_user_model_import():
    assert User is not None


@pytest.mark.asyncio
async def test_user_profile_model_import():
    assert UserProfile is not None
