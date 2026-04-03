from dataclasses import dataclass

from .app_constants import AppConstants
from .cors_constants import CORSConstants


@dataclass(frozen=True)
class Constants(
    CORSConstants,
    AppConstants,
):
    """Root constants class — inherits all child constant modules."""

    pass


constants = Constants()
