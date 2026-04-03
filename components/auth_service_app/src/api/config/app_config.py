from pydantic import field_validator
from pydantic_settings import BaseSettings

from src.api.constants import constants


class AppSettings(BaseSettings):
    """Application-level settings (logging, service name)."""

    LOG_LEVEL: str = "INFO"
    SERVICE_NAME: str = "auth-service"

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        if value not in constants.VALID_LOG_LEVELS:
            raise ValueError(f"Invalid LOGLEVEL: {value}. Choose from {constants.VALID_LOG_LEVELS}")
        return value
