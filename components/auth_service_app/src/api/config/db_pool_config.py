from pydantic_settings import BaseSettings


class DBPoolSettings(BaseSettings):
    """SQLAlchemy async connection-pool configuration."""

    DB_POOL_SIZE: int = 15
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_ISOLATION_LEVEL: str = "READ COMMITTED"
    DB_POOL_PRE_PING: bool = True
