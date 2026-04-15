from pydantic import BaseModel


class SessionStatusResponseDTO(BaseModel):
    user_id: str | None = None
    message: str | None = None
