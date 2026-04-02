from functools import lru_cache
from src.api.config import Settings


@lru_cache
def Config():
    """Dependency that returns the application settings instance (singleton)."""
    return Settings()
