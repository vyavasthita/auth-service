from pydantic import BaseModel, Field


class RegisterUserRequestDTO(BaseModel):
    # DTO for user registration request payload.
    username: str = Field(
        description="Username of the user.",
        json_schema_extra={"example": "dilip_sharma"},
    )
    password: str = Field(
        description="Password of the user.",
    )
