from pydantic import BaseModel, EmailStr, Field


class LoginUserRequestDTO(BaseModel):
    # DTO for user login request payload.
    email: EmailStr = Field(
        description="Email ID of the user.",
        json_schema_extra={"example": "dilip@gmail.com"},
    )

    password: str = Field(
        description="Password of the user.",
    )
