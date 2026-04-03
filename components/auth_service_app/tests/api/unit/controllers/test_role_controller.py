import pytest

from src.api.controllers import role_router


@pytest.mark.asyncio
async def test_role_controller_import():
    assert role_router is not None


def test_role_controller_registers_add_role_route():
    routes = {route.path for route in role_router.routes}
    assert "/roles" in routes


def test_role_controller_add_role_is_post():
    route = next(r for r in role_router.routes if r.path == "/roles")
    assert "POST" in route.methods
