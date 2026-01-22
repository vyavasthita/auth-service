from pydantic import BaseModel, Field


class RegisterUserRequestDTO(BaseModel):
    name: str = Field(
        description="Name of the user.",
        json_schema_extra={"example": "Dilip Sharma"},
    )

    email: str = Field(
        description="Email ID of the user.",
        json_schema_extra={"example": "dilip@gmail.com"},
    )

    password: str = Field(
        description="Password of the user.",
    )

    phone_number: str = Field(
        description="Phone Number of the user.",
        json_schema_extra={"example": "9876543210"},
    )