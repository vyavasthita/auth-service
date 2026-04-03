from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controllers import auth_router
from src.api.exceptions import InvalidTokenException, register_exception_handlers
from src.api.services import AuthServiceImpl


@pytest.fixture
def client():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(auth_router)
    return TestClient(app)


def test_validate_token_valid(client, monkeypatch):
    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_user = MagicMock()
    mock_user.user_id = test_uuid.bytes
    mock_user.username = "dilip_sharma"

    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(return_value=mock_user),
    )
    response = client.post("/validate", cookies={"access_token": "validtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == str(test_uuid)
    assert data["username"] == "dilip_sharma"


def test_validate_token_missing_cookie(client):
    response = client.post("/validate")
    assert response.status_code == 401


def test_validate_token_invalid(client, monkeypatch):
    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(side_effect=InvalidTokenException()),
    )
    response = client.post("/validate", cookies={"access_token": "badtoken"})
    assert response.status_code == 401
