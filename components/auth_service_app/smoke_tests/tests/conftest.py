import os

import httpx
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL")
