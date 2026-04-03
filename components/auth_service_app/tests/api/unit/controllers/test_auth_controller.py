import pytest

from src.api.controllers import auth_router


@pytest.mark.asyncio
async def test_auth_controller_import():
    assert auth_router is not None


def test_auth_controller_registers_login_route():
    routes = {route.path for route in auth_router.routes}
    assert "/login" in routes
