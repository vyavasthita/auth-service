import pytest

from src.api.dtos import RegisterUserResponseDTO


@pytest.mark.asyncio
async def test_register_user_response_dto_fields():
    dto = RegisterUserResponseDTO(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone_number="1234567890",
    )
    assert dto.first_name == "Test"
    assert dto.last_name == "User"
    assert dto.email == "test@example.com"
    assert dto.phone_number == "1234567890"
