from pydantic import BaseModel, Field


class AddRoleResponseDTO(BaseModel):
    # DTO for role addition response payload.
    message: str = Field(
        default="Role added successfully.",
        description="A message indicating the result of the role addition.",
    )
