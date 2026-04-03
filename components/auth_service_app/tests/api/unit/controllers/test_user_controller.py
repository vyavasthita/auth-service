from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controllers import user_router
from src.api.exceptions import InvalidTokenException, register_exception_handlers
from src.api.services import AuthServiceImpl


@pytest.fixture
def client():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(user_router)
    return TestClient(app)


def test_user_controller_import():
    assert user_router is not None


def test_user_controller_registers_me_route():
    routes = {route.path for route in user_router.routes}
    assert "/users/me" in routes


def test_user_controller_me_is_get():
    route = next(r for r in user_router.routes if r.path == "/users/me")
    assert "GET" in route.methods


def test_get_me_valid(client, monkeypatch):
    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_user = MagicMock()
    mock_user.user_id = test_uuid.bytes
    mock_user.username = "dilip_sharma"
    mock_user.created_at = datetime(2026, 1, 1, 0, 0, 0)

    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(return_value=mock_user),
    )
    response = client.get("/users/me", cookies={"access_token": "validtoken"}, params={"user_id": str(test_uuid)})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == str(test_uuid)
    assert data["username"] == "dilip_sharma"
    assert "created_at" in data


def test_get_me_missing_cookie(client):
    response = client.get("/users/me", params={"user_id": "12345678-1234-5678-1234-567812345678"})
    assert response.status_code == 401


def test_get_me_invalid_token(client, monkeypatch):
    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(side_effect=InvalidTokenException()),
    )
    response = client.get(
        "/users/me", cookies={"access_token": "badtoken"}, params={"user_id": "12345678-1234-5678-1234-567812345678"}
    )
    assert response.status_code == 401
