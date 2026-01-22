import pytest
from auth_service_app.api.controllers import AuthController


@pytest.mark.asyncio
async def test_auth_controller_import():
    assert AuthController() is not None


def test_auth_controller_registers_login_route():
    controller = AuthController()
    routes = {route.path for route in controller.router.routes}
    assert "/login" in routes