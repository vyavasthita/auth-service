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


def test_check_session_status_active(client, monkeypatch):
    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_user = MagicMock()
    mock_user.user_id = test_uuid.bytes
    mock_user.username = "dilip_sharma"

    monkeypatch.setattr(
        AuthServiceImpl,
        "check_session_status",
        AsyncMock(return_value=mock_user),
    )
    client.cookies.set("access_token", "validtoken")
    response = client.post("/session-status", params={"user_id": str(test_uuid)})
    client.cookies.clear()
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == str(test_uuid)


def test_check_session_status_missing_cookie(client):
    response = client.post("/session-status", params={"user_id": "12345678-1234-5678-1234-567812345678"})
    assert response.status_code == 422


def test_check_session_status_inactive(client, monkeypatch):
    monkeypatch.setattr(
        AuthServiceImpl,
        "check_session_status",
        AsyncMock(side_effect=InvalidTokenException()),
    )
    client.cookies.set("access_token", "badtoken")
    response = client.post("/session-status", params={"user_id": "12345678-1234-5678-1234-567812345678"})
    client.cookies.clear()
    assert response.status_code == 401
