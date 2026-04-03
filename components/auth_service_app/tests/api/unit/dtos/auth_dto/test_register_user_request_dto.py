import pytest

from src.api.dtos import RegisterUserRequestDTO


@pytest.mark.asyncio
async def test_register_user_request_dto_fields():
    dto = RegisterUserRequestDTO(
        username="test_user",
        password="password123",
    )
    assert dto.username == "test_user"
    assert dto.password == "password123"
