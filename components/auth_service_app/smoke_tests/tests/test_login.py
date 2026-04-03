import pytest


@pytest.mark.asyncio
async def test_login_user(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"

    shared_email = "smoke-user@gmail.com"
    password = "secret"

    register_payload = {
        "first_name": "Smoke",
        "last_name": "Test User",
        "email": shared_email,
        "password": password,
        "phone_number": "9876543210",
    }

    register_response = await async_client.post(register_url, json=register_payload)
    assert register_response.status_code in [201, 409], (
        f"Register failed: {register_response.status_code}"
    )

    login_payload = {
        "email": shared_email,
        "password": password,
    }

    login_response = await async_client.post(login_url, json=login_payload)
    assert login_response.status_code == 200, (
        f"Login failed: {login_response.status_code}, body={login_response.text}"
    )

    body = login_response.json()
    assert body.get("message") == "Login successful."
    assert "access_token" in login_response.cookies, "access_token cookie missing in response"
