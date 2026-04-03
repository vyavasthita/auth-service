from pydantic import BaseModel


class ValidateTokenResponseDTO(BaseModel):
    user_id: str | None = None
    email: str | None = None
    message: str | None = None
