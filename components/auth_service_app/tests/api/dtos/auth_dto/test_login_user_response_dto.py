import pytest

from src.api.dtos import LoginUserResponseDTO


@pytest.mark.asyncio
async def test_login_user_response_dto_fields():
    dto = LoginUserResponseDTO(access_token="token", token_type="bearer")
    assert dto.access_token == "token"
    assert dto.token_type == "bearer"
