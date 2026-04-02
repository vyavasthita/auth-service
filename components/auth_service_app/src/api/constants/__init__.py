from dataclasses import dataclass
from .cors_constants import CORSConstants
from .app_constants import AppConstants


@dataclass(frozen=True)
class Constants(
    CORSConstants,
    AppConstants,
):
    """Root constants class — inherits all child constant modules."""
    pass


constants = Constants()
