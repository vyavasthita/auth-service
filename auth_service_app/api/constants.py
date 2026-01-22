from dataclasses import dataclass, field
from typing import List

"""This module defines project-level constants."""


@dataclass(frozen=True)
class ConstantsNamespace:
    """
    The HTTP Access-Control-Allow-Methods response header specifies one or more HTTP request methods 
    allowed when accessing a resource in response to a preflight request.
    """
    CORS_ALLOW_METHODS: List = field(default_factory=lambda: ["OPTIONS", "GET", "POST"])

    """
    The HTTP Access-Control-Allow-Headers response header is used in response to a 
    preflight request to indicate the HTTP headers that can be used during the actual request. 
    
    This header is required if the preflight request contains Access-Control-Request-Headers.
    """
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