from pydantic import BaseModel


class ValidateTokenRequestDTO(BaseModel):
    user_id: str
    token: str
