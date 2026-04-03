from pydantic import BaseModel, Field


class RegisterUserResponseDTO(BaseModel):
    # DTO for user registration response payload.
    username: str = Field(
        description="Username of the user.",
        json_schema_extra={"example": "dilip_sharma"},
    )
    email: str = Field(
        description="Email of the user.",
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
    phone_number: str = Field(
        description="Phone number of the user.",
        json_schema_extra={"example": "9876543210"},
    )
