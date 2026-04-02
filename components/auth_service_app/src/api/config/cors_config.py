from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class CORSSettings(BaseSettings):
    """CORS settings."""

    ALLOW_ORIGINS: Optional[str] = "http://127.0.0.1:5001"

    @field_validator("ALLOW_ORIGINS")
    def assemble_cors_origins(cls, value: str) -> Union[List[str], str]:
        return [value]

    ALLOW_CREDENTIALS: bool = True
    MAX_AGE: Optional[int] | None = 60
