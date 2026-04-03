import pytest


@pytest.mark.asyncio
async def test_register_user(base_url, async_client):
    url = f"{base_url}/register"

    payload = {
        "name": "Test User",
        "email": "testuser@gmail.com",
        "password": "secret",
        "phone_number": "9876543210"
    }

    response = await async_client.post(url, json=payload)
    assert response.status_code in [201, 409], f"POST failed: {response.status_code}"
