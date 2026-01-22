import pytest
from auth_service_app.api.exceptions import DBConnectionException


@pytest.mark.asyncio
async def test_db_connection_exception_message():
    exc = DBConnectionException()
    assert exc.message == "Internal Server Error."
