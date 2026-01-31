from pydantic import BaseModel


class ValidateTokenResponseDTO(BaseModel):
    is_valid: bool = True
    email: str | None = None
    message: str | None = None
