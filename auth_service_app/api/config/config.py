from typing import List, Optional, Union
from pydantic import field_validator, BaseModel
from pydantic_settings import BaseSettings
from api.constants import constants


class MySQLSettings(BaseModel):
    CA_CERT_PATH: str = ""
    USE_SSL: str | None = ""
    MYSQL_HOST: str | None = ""
    MYSQL_DATABASE: str | None = ""
    MYSQL_USER: str | None = ""
    MYSQL_PASSWORD: str | None = ""
    CONNECT_TIMEOUT: int = 5  # Connection timeout in seconds


class ObservabilitySettings(BaseModel):
    OTEL_SERVICE_NAME: str = "auth-service"
    LOGGING_BACKEND: str = "opensearch"
    TRACING_BACKEND: str = "tempo"
    METRICS_BACKEND: str = "prometheus"
    RATE_LIMITED_LOG_INTERVAL_SECONDS: int = 60


class CORSSettings(BaseModel):
    """
    The HTTP Access-Control-Allow-Origin response header indicates whether the response 
    can be shared with requesting code from the given origin.
    """
    ALLOW_ORIGINS: Optional[str] = "http://127.0.0.1:5000"

    """
    The HTTP Access-Control-Allow-Credentials response header tells browsers whether 
    the server allows credentials to be included in cross-origin HTTP requests.
    """
    ALLOW_CREDENTIALS: bool = True

    """
    The HTTP Access-Control-Max-Age response header indicates how long the results of a preflight request 
    (that is, the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached.
    """
    MAX_AGE: Optional[int] | None = 60  # Seconds

    @field_validator("ALLOW_ORIGINS")
    def assemble_cors_origins(cls, value: str) -> Union[List[str], str]:
        return [value]

class OpenAPISettings(BaseModel):
    ENABLE_SWAGGER_UI: bool | None = True
    OPEN_API_DOCS_URL: Optional[str] | None = "/docs"
    OPEN_API_RE_DOC_URL: Optional[str] | None = "/redoc"

class OtherSettings(BaseModel):
    LOG_LEVEL: str = "INFO"

    @field_validator("LOG_LEVEL")
    def validate_log_level(cls, value: str) -> str:
        if value not in constants.VALID_LOG_LEVELS:
            raise ValueError(
                f"Invalid LOGLEVEL: {value}. Choose from {constants.VALID_LOG_LEVELS}"
            )
        return value

class Settings(MySQLSettings, ObservabilitySettings, CORSSettings, OpenAPISettings, OtherSettings, BaseSettings):
    """Application settings, composed from multiple config classes."""
    pass