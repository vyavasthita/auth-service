import pytest

from src.api.dtos import RegisterUserResponseDTO


@pytest.mark.asyncio
async def test_register_user_response_dto_fields():
    dto = RegisterUserResponseDTO(
        username="test_user",
    )
    assert dto.username == "test_user"
