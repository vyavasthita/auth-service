"""
Root conftest for auth-service functional tests.

Key Components:
    1. DummySession: ORM-compatible mock session (add, get, flush, merge, delete).
    2. async_client: httpx.AsyncClient hitting FastAPI ASGI app, DB dependency overridden.
    3. pytest_generate_tests: JSON-driven parameterization via @pytest.mark.test_section.
"""

import os
import sys
from unittest.mock import MagicMock

import httpx
import pytest
import pytest_asyncio

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so ``import src`` resolves correctly
# even when pytest is invoked from a different working directory.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Set minimal env vars BEFORE any app-level imports.
# These satisfy pydantic-settings validation without a real database.
# ---------------------------------------------------------------------------
os.environ.setdefault("SERVICE_NAME", "auth-service")
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_DATABASE", "test")
os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")

# Prevent real MySQL engine creation during import
from unittest.mock import patch as _patch  # noqa: E402

from src.api.repos.db import DatabaseEngine  # noqa: E402

DatabaseEngine._engine_instance = None  # reset singleton
_engine_patcher = _patch.object(DatabaseEngine, "_create_engine", return_value=MagicMock())
_engine_patcher.start()

from src.api import app  # noqa: E402
from src.api.dependencies.db_dependency import DatabaseDependency  # noqa: E402
from tests.api.common.data_helper import get_test_cases_from_section, load_json_data  # noqa: E402


# ---------------------------------------------------------------------------
# DummySession
# ---------------------------------------------------------------------------
class DummyResult:
    """Mock for SQLAlchemy Result (supports .scalars().all() and .scalar_one_or_none() chains)."""

    def __init__(self, rows=None):
        self._rows = rows or []

    def scalars(self):
        return self

    def all(self):
        return self._rows

    def first(self):
        return self._rows[0] if self._rows else None

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None


class DummySession:
    """ORM-compatible async mock session."""

    def __init__(self):
        self._added = []

    def add(self, entity):
        self._added.append(entity)

    async def get(self, model, pk):
        return None

    async def flush(self):
        pass

    async def refresh(self, entity, attribute_names=None):
        pass

    async def merge(self, entity):
        return entity

    async def delete(self, entity):
        pass

    async def execute(self, stmt, params=None):
        return DummyResult()

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def db_session():
    """Default DummySession."""
    return DummySession()


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session):
    """Async httpx client wired to the FastAPI app with DB dependency overridden."""

    async def override_get_db_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[DatabaseDependency.get_db_session] = override_get_db_session

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.pop(DatabaseDependency.get_db_session, None)


@pytest.fixture
def anyio_backend():
    return "asyncio"


# ---------------------------------------------------------------------------
# Markers and Parameterization
# ---------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "test_section(name): Link test function to a JSON section.")


def pytest_generate_tests(metafunc):
    """Dynamically parameterizes tests from JSON via @pytest.mark.test_section."""

    marker = metafunc.definition.get_closest_marker("test_section")
    if not marker:
        return

    section_name = marker.args[0]
    test_data_file = getattr(metafunc.module, "TEST_DATA_FILE", None)

    if not test_data_file:
        pytest.skip(f"{metafunc.module.__name__} does not define TEST_DATA_FILE")

    base_dir = metafunc.definition.fspath.dirname
    json_data = load_json_data(base_dir, test_data_file)
    test_cases = get_test_cases_from_section(json_data, section_name)

    # Use description field for readable test IDs when present
    ids = [getattr(tc, "description", None) or f"{section_name}[{i}]" for i, tc in enumerate(test_cases)]
    metafunc.parametrize("test_case", test_cases, ids=ids)
