import pytest

from src.api.dtos import LoginUserRequestDTO


@pytest.mark.asyncio
async def test_login_user_request_dto_fields():
    dto = LoginUserRequestDTO(username="dilip_sharma", password="password123")
    assert dto.username == "dilip_sharma"
    assert dto.password == "password123"
