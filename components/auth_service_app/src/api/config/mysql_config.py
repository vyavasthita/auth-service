from pydantic_settings import BaseSettings


class MySQLSettings(BaseSettings):
    """MySQL connection settings."""

    CA_CERT_PATH: str = ""
    USE_SSL: str | None = ""
    MYSQL_HOST: str | None = ""
    MYSQL_DATABASE: str | None = ""
    MYSQL_USER: str | None = ""
    MYSQL_PASSWORD: str | None = ""
    CONNECT_TIMEOUT: int = 5
