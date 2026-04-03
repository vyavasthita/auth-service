from pydantic import BaseModel, Field


class LoginUserResponseDTO(BaseModel):
    # DTO for user login response payload.
    message: str = Field(
        default="Login successful.",
        description="A message indicating the result of the login attempt.",
    )
