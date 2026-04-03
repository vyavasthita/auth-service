import pytest


@pytest.mark.asyncio
async def test_health(base_url, async_client):
    response = await async_client.get(base_url + "/health")
    assert response.status_code == 200
