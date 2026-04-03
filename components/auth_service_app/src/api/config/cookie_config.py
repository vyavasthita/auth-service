from pydantic_settings import BaseSettings


class CookieSettings(BaseSettings):
    """Cookie settings for authentication tokens."""

    COOKIE_NAME: str = "access_token"
    COOKIE_HTTPONLY: bool = True
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "lax"
    COOKIE_PATH: str = "/"
