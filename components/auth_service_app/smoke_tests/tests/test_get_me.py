import pytest


@pytest.mark.asyncio
async def test_get_me_smoke(base_url, async_client):
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    me_url = f"{base_url}/users/me"

    shared_username = "smoke_me_user"
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

    me_response = await async_client.get(
        me_url,
        cookies={"access_token": token},
        params={"user_id": user_id},
    )
    assert me_response.status_code == 200, (
        f"GET /users/me failed: {me_response.status_code}"
    )

    body = me_response.json()
    assert body["username"] == shared_username
    assert "user_id" in body
    assert "created_at" in body


@pytest.mark.asyncio
async def test_get_me_no_token_smoke(base_url, async_client):
    me_url = f"{base_url}/users/me"

    response = await async_client.get(
        me_url,
        params={"user_id": "00000000-0000-0000-0000-000000000000"},
    )
    assert response.status_code == 401, (
        f"Expected 401 without token, got: {response.status_code}"
    )
