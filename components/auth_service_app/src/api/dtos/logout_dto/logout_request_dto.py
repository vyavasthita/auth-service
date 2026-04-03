from pydantic import BaseModel, Field


class LogoutRequestDTO(BaseModel):
    # DTO for logout request payload.
    user_id: str = Field(
        description="UUID of the user.",
        json_schema_extra={"example": "12345678-1234-5678-1234-567812345678"},
    )
    token: str = Field(
        description="JWT access token.",
        json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIs..."},
    )
