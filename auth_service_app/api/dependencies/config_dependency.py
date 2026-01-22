from functools import lru_cache
from api.config import Settings


@lru_cache
def Config():
    return Settings()