import pytest

from src.api.dtos import LoginUserResponseDTO


@pytest.mark.asyncio
async def test_login_user_response_dto_fields():
    dto = LoginUserResponseDTO(user_id="550e8400-e29b-41d4-a716-446655440000")
    assert dto.message == "Login successful."
    assert dto.user_id == "550e8400-e29b-41d4-a716-446655440000"
