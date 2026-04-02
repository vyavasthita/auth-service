from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    """JWT authentication settings."""

    SECRET_KEY: str = "auth-service-secret"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 10
