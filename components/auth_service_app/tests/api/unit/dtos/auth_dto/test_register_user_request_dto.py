import pytest

from src.api.dtos import RegisterUserRequestDTO


@pytest.mark.asyncio
async def test_register_user_request_dto_fields():
    dto = RegisterUserRequestDTO(
        username="test_user",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="password123",
        phone_number="1234567890",
    )
    assert dto.username == "test_user"
    assert dto.first_name == "Test"
    assert dto.last_name == "User"
    assert dto.email == "test@example.com"
    assert dto.password == "password123"
    assert dto.phone_number == "1234567890"
