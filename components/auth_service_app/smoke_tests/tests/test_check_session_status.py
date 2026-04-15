import pytest


@pytest.mark.asyncio
async def test_check_session_status_smoke(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    session_status_url = f"{base_url}/session-status"

    shared_username = "smoke_session_status_user"
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

    session_status_response = await async_client.post(
        session_status_url,
        cookies={"access_token": token},
        params={"user_id": user_id},
    )
    assert session_status_response.status_code == 200, (
        f"Session status check failed: {session_status_response.status_code}"
    )

    data = session_status_response.json()
    assert data["user_id"] == user_id
    assert data["message"] == "Session is active."
