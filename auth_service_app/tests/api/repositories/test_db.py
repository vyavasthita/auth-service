import pytest
from auth_service_app.api.dependencies import get_db_session


@pytest.mark.asyncio
async def test_get_db_session_import():
    assert get_db_session is not None
