import pytest

from src.api.dtos import LoginUserResponseDTO


@pytest.mark.asyncio
async def test_login_user_response_dto_fields():
    dto = LoginUserResponseDTO()
    assert dto.message == "Login successful."
