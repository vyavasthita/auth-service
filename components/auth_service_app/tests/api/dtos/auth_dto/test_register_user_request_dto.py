import pytest
from src.api.dtos import RegisterUserRequestDTO


@pytest.mark.asyncio
async def test_register_user_request_dto_fields():
    dto = RegisterUserRequestDTO(
        name="Test User",
        email="test@example.com",
        password="password123",
        phone_number="1234567890"
    )
    assert dto.name == "Test User"
    assert dto.email == "test@example.com"
    assert dto.password == "password123"
    assert dto.phone_number == "1234567890"
