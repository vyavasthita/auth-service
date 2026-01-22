import pytest
from auth_service_app.api.dtos import LoginUserRequestDTO


@pytest.mark.asyncio
async def test_login_user_request_dto_fields():
    dto = LoginUserRequestDTO(email="test@example.com", password="password123")
    assert dto.email == "test@example.com"
    assert dto.password == "password123"
