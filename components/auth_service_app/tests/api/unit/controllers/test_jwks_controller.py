"""Unit tests for the JWKS controller endpoint."""

from unittest.mock import MagicMock, patch

import pytest

from src.api.controllers import jwks_router


def test_jwks_controller_import():
    assert jwks_router is not None


def test_jwks_controller_registers_route():
    routes = {route.path for route in jwks_router.routes}
    assert "/token/.well-known/jwks.json" in routes


@pytest.mark.asyncio
async def test_get_jwks_returns_keys():
    """GET /.well-known/jwks.json returns JWKS structure with Cache-Control."""
    from fastapi import FastAPI
    from httpx import ASGITransport, AsyncClient

    app = FastAPI()
    app.include_router(jwks_router)

    fake_jwks = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "test-kid",
                "use": "sig",
                "alg": "RS256",
                "n": "abc",
                "e": "AQAB",
            }
        ]
    }

    with patch("src.api.controllers.jwks_controller.KeyManager") as mock_km_cls:
        mock_km = MagicMock()
        mock_km.get_jwks.return_value = fake_jwks
        mock_km_cls.return_value = mock_km

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/token/.well-known/jwks.json")

    assert response.status_code == 200
    assert response.json() == fake_jwks
    assert "public" in response.headers.get("cache-control", "")
