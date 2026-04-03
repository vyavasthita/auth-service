import pytest


@pytest.mark.asyncio
async def test_validate_token_smoke(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    validate_url = f"{base_url}/validate"

    shared_username = "smoke_validate_user"
    password = "smokepass123"

    register_payload = {
        "username": shared_username,
        "password": password,
    }

    register_response = await async_client.post(register_url, json=register_payload)
    assert register_response.status_code in [201, 409], (
        f"Register failed: {register_response.status_code}"
    )

    login_response = await async_client.post(login_url, json={
        "username": shared_username,
        "password": password,
    })
    assert login_response.status_code == 200, (
        f"Login failed: {login_response.status_code}"
    )

    token = login_response.cookies["access_token"]
    user_id = login_response.json()["user_id"]

    validate_response = await async_client.post(
        validate_url,
        cookies={"access_token": token},
        params={"user_id": user_id},
    )
    assert validate_response.status_code == 200, (
        f"Validate token failed: {validate_response.status_code}"
    )

    data = validate_response.json()
    assert data["username"] == shared_username
