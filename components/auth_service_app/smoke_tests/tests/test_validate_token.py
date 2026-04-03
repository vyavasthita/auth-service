import pytest


@pytest.mark.asyncio
async def test_validate_token_smoke(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    validate_url = f"{base_url}/validate"

    shared_email = "smoke-validate-user@gmail.com"
    shared_username = "smoke_validate_user"
    password = "smokepass123"

    register_payload = {
        "username": shared_username,
        "first_name": "Smoke",
        "last_name": "Validate User",
        "email": shared_email,
        "password": password,
        "phone_number": "1234567890",
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

    validate_response = await async_client.post(
        validate_url,
        cookies={"access_token": token},
    )
    assert validate_response.status_code == 200, (
        f"Validate token failed: {validate_response.status_code}"
    )

    data = validate_response.json()
    assert data["username"] == shared_username
