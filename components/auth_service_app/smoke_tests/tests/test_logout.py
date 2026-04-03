import pytest


@pytest.mark.asyncio
async def test_logout_smoke(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    logout_url = f"{base_url}/logout"

    shared_username = "smoke_logout_user"
    password = "smokepass123"

    register_response = await async_client.post(register_url, json={
        "username": shared_username,
        "password": password,
    })
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

    logout_response = await async_client.post(
        logout_url,
        json={"user_id": user_id, "token": token},
    )
    assert logout_response.status_code == 200, (
        f"Logout failed: {logout_response.status_code}"
    )

    body = logout_response.json()
    assert body["message"] == "Logged out successfully."
