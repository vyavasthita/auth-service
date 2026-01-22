import pytest


@pytest.mark.asyncio
async def test_health(base_url, async_client):
    response = await async_client.get(base_url + "/app_health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_db_health(base_url, async_client):
    response = await async_client.get(base_url + "/db_health")
    assert response.status_code == 200