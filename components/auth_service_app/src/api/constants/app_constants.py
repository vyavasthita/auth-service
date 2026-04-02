from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class AppConstants:
    """Service-level constants (logging levels)."""

    VALID_LOG_LEVELS: List = field(
        default_factory=lambda: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )
