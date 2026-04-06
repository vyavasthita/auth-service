from pydantic import field_validator
from pydantic_settings import BaseSettings


class CORSSettings(BaseSettings):
    """CORS settings."""

    ALLOW_ORIGINS: str | None = "http://127.0.0.1:2001"

    @field_validator("ALLOW_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, value: str) -> list[str] | str:
        return [value]

    ALLOW_CREDENTIALS: bool = True
    MAX_AGE: int | None | None = 60
