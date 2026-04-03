from unittest.mock import AsyncMock, MagicMock

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
    mock_user = MagicMock()
    mock_user.email = "user@gmail.com"

    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(return_value=mock_user),
    )
    response = client.post("/validate-token", json={"token": "validtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert data["email"] == "user@gmail.com"
    assert data["message"] == "Token is valid."


def test_validate_token_invalid(client, monkeypatch):
    monkeypatch.setattr(
        AuthServiceImpl,
        "validate_token",
        AsyncMock(side_effect=InvalidTokenException()),
    )
    response = client.post("/validate-token", json={"token": "badtoken"})
    assert response.status_code == 401
