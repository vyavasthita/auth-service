import pytest
from fastapi.testclient import TestClient
from src.api.controllers import auth_router
from fastapi import FastAPI
from src.api.dtos import ValidateTokenRequestDTO

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(auth_router)
    return TestClient(app)


def test_validate_token_valid(client, monkeypatch):
    # Patch AuthServiceImpl.validate_token to always return claims
    monkeypatch.setattr(
        "src.api.services.auth_service.auth_service_impl.AuthServiceImpl.validate_token",
        lambda self, token: {"sub": "user@example.com"}
    )
    response = client.post("/validate-token", json={"token": "validtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert data["user_id"] == "user@example.com"
    assert data["message"] == "Token is valid."


def test_validate_token_invalid(client, monkeypatch):
    # Patch AuthServiceImpl.validate_token to raise Exception
    def raise_exc(self, token):
        raise Exception("Invalid or expired token.")
    monkeypatch.setattr(
        "src.api.services.auth_service.auth_service_impl.AuthServiceImpl.validate_token",
        raise_exc
    )
    response = client.post("/validate-token", json={"token": "badtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert data["user_id"] is None
    assert "Invalid or expired token" in data["message"]
