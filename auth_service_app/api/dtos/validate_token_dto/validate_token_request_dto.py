from pydantic import BaseModel


class ValidateTokenRequestDTO(BaseModel):
    token: str
