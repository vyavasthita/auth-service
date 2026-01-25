from dataclasses import dataclass, field
from typing import List




@dataclass(frozen=True)
class ConstantsNamespace:
    CORS_ALLOW_METHODS: List = field(default_factory=lambda: ["OPTIONS", "GET", "POST"])
    CORS_ALLOW_HEADERS: List = field(
        default_factory=lambda: ["Content-Type", "Authorization"]
    )

    VALID_LOG_LEVELS: List = field(
        default_factory=lambda: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )

    # Connection pool constants

    # pool_size: steady open connections sized for expected concurrent requests.
    DB_POOL_SIZE: int = 15

    # max_overflow: temporary extra connections allowed above pool_size for bursts.
    DB_MAX_OVERFLOW: int = 10

    # pool_timeout: seconds to wait for a free connection before failing fast.
    DB_POOL_TIMEOUT: int = 10

    # pool_recycle: recycle connections before MySQL wait_timeout to avoid stale sockets.
    DB_POOL_RECYCLE: int = 3600

    # isolation_level: transaction isolation; READ COMMITTED reduces locking vs REPEATABLE READ.
    DB_ISOLATION_LEVEL: str = "READ COMMITTED"

    # pool_pre_ping: proactively checks liveness to prevent 'MySQL server has gone away'.
    DB_POOL_PRE_PING: bool = True


constants = ConstantsNamespace()