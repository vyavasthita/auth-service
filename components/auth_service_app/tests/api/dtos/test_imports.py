import pytest
import importlib
import pkgutil
from src.api import dtos as api_dtos


@pytest.mark.asyncio
async def test_import_all_dtos():
    # Recursively import all modules in auth_service_app.api.dtos
    for finder, name, ispkg in pkgutil.walk_packages(api_dtos.__path__, api_dtos.__name__ + "."):
        module = importlib.import_module(name)
        assert module is not None
