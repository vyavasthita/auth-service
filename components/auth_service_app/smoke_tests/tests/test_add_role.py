import uuid

import pytest


@pytest.mark.asyncio
async def test_add_role_smoke(base_url, async_client):
    url = f"{base_url}/roles"

    # Use a unique role name to avoid conflicts across runs
    role_name = f"smoke_role_{uuid.uuid4().hex[:8]}"

    response = await async_client.post(url, json={"role_name": role_name})
    assert response.status_code == 201, (
        f"POST /roles failed: {response.status_code}, body={response.text}"
    )

    body = response.json()
    assert body["message"] == f"Role '{role_name}' added successfully."


@pytest.mark.asyncio
async def test_add_role_duplicate_smoke(base_url, async_client):
    url = f"{base_url}/roles"

    role_name = f"smoke_dup_role_{uuid.uuid4().hex[:8]}"

    first = await async_client.post(url, json={"role_name": role_name})
    assert first.status_code == 201

    second = await async_client.post(url, json={"role_name": role_name})
    assert second.status_code == 409, (
        f"Expected 409 for duplicate role, got: {second.status_code}"
    )
