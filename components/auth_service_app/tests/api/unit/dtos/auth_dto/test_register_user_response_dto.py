import pytest

from src.api.dtos import RegisterUserResponseDTO


@pytest.mark.asyncio
async def test_register_user_response_dto_fields():
    dto = RegisterUserResponseDTO(name="Test User", email="test@example.com", phone_number="1234567890")
    assert dto.name == "Test User"
    assert dto.email == "test@example.com"
    assert dto.phone_number == "1234567890"
