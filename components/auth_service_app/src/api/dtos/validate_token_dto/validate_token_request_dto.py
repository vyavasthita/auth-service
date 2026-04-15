from pydantic import BaseModel


class SessionStatusRequestDTO(BaseModel):
    user_id: str
    token: str
