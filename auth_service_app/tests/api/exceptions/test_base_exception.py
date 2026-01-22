import pytest
from auth_service_app.api.exceptions import BaseException


@pytest.mark.asyncio
async def test_base_exception_message():
    exc = BaseException(400, "test message")
    assert exc.message == "test message"
