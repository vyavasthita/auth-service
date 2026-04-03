from pydantic import BaseModel, Field


class RegisterUserRequestDTO(BaseModel):
    # DTO for user registration request payload.
    email: str = Field(
        description="Email ID of the user.",
        json_schema_extra={"example": "dilip@gmail.com"},
    )
    first_name: str = Field(
        description="First name of the user.",
        json_schema_extra={"example": "Dilip"},
    )
    last_name: str = Field(
        description="Last name of the user.",
        json_schema_extra={"example": "Sharma"},
    )
    password: str = Field(
        description="Password of the user.",
    )
    phone_number: str = Field(
        description="Phone Number of the user.",
        json_schema_extra={"example": "9876543210"},
    )
