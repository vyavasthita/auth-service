from pydantic import BaseModel, Field


class LoginUserResponseDTO(BaseModel):
    # DTO for user login response payload containing the access token.
    access_token: str = Field(
        description="Bearer token issued after successful authentication.",
    )

    token_type: str = Field(
        default="bearer",
        description="Type of the issued token.",
    )
