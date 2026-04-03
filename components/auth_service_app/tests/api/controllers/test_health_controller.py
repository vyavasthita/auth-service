import pytest
from src.api.controllers import health_router


def test_health_router_import():
    assert health_router is not None


def test_health_router_registers_health_route():
    routes = {route.path for route in health_router.routes}
    assert "/health" in routes