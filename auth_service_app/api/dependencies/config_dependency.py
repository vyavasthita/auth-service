from functools import lru_cache
from api.config import Settings


@lru_cache
def Config():
    """
    Dependency that returns the application settings instance (singleton).

    Returns:
        Settings: The application settings object.
    """
    return Settings()