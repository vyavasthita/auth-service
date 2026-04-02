from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class CORSConstants:
    """CORS-related constants."""

    CORS_ALLOW_METHODS: List = field(default_factory=lambda: ["OPTIONS", "GET", "POST"])
    CORS_ALLOW_HEADERS: List = field(
        default_factory=lambda: ["Content-Type", "Authorization"]
    )
