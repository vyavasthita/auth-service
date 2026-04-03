from dataclasses import dataclass, field


@dataclass(frozen=True)
class AppConstants:
    """Service-level constants (logging levels)."""

    VALID_LOG_LEVELS: list = field(default_factory=lambda: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
