from pydantic import BaseModel, Field


class AddRoleRequestDTO(BaseModel):
    # DTO for adding a new role.
    role_name: str = Field(
        description="Name of the role.",
        json_schema_extra={"example": "admin"},
    )
