from pydantic import BaseModel, Field


class RegisterUserResponseDTO(BaseModel):
    # DTO for user registration response payload.
    username: str = Field(
        description="Username of the user.",
        json_schema_extra={"example": "dilip_sharma"},
    )
