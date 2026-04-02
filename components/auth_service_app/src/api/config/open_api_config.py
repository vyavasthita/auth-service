from typing import Optional
from pydantic_settings import BaseSettings


class OpenAPISettings(BaseSettings):
    """OpenAPI / Swagger UI documentation settings."""

    ENABLE_SWAGGER_UI: bool | None = True
    OPEN_API_DOCS_URL: Optional[str] | None = "/docs"
    OPEN_API_RE_DOC_URL: Optional[str] | None = "/redoc"
