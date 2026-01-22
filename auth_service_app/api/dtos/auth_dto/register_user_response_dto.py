from pydantic import BaseModel, Field


class RegisterUserResponseDTO(BaseModel):
    name: str = Field(
        description="Name of the user.",
        json_schema_extra={"example": "Dilip Sharma"},
    )

    email: str = Field(
        description="Email of the user.",
        json_schema_extra={"example": "dilip.sharma@example.com"},
    )

    phone_number: str = Field(
        description="Phone number of the user.",
        json_schema_extra={"example": "9876543210"},
    )