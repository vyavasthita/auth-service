import base64
import json
import os

import httpx
import pytest
import pytest_asyncio


def decode_jwt_payload(token: str) -> dict:
    """Decode a JWT payload without signature verification (stdlib only)."""
    payload = token.split(".")[1]
    payload += "=" * (4 - len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL")
