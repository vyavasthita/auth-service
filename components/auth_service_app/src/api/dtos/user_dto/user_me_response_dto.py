from pydantic import BaseModel, Field


class UserMeResponseDTO(BaseModel):
    # DTO for GET /users/me response payload.
    user_id: str = Field(description="UUID of the user.")
    username: str = Field(description="Username of the user.")
    created_at: str = Field(description="Timestamp when the user was created.")
