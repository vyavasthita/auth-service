from pydantic import BaseModel


class ValidateTokenResponseDTO(BaseModel):
    user_id: str | None = None
    username: str | None = None
    message: str | None = None
