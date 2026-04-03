import pytest

from src.api.dependencies import DatabaseDependency


@pytest.mark.asyncio
async def test_get_db_session_import():
    assert DatabaseDependency.get_db_session is not None
