from dataclasses import dataclass, field


@dataclass(frozen=True)
class CORSConstants:
    """CORS-related constants."""

    CORS_ALLOW_METHODS: list = field(default_factory=lambda: ["OPTIONS", "GET", "POST"])
    CORS_ALLOW_HEADERS: list = field(default_factory=lambda: ["Content-Type", "Authorization"])
