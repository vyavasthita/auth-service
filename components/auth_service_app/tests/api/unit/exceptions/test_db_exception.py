import pytest

from src.api.exceptions import DBException


@pytest.mark.asyncio
async def test_db_connection_exception_message():
    exc = DBException()
    assert exc.message == "Internal Server Error."
