from threading import Lock
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from api.constants import constants
from api.dependencies import Config


class BaseDB:
    _engine_lock = Lock()
    _engine_instance: AsyncEngine | None = None

    def _build_connect_args(self):
        args = {"connect_timeout": Config().CONNECT_TIMEOUT}

        # aiomysql expects an ssl.SSLContext, not a plain dict
        if Config().USE_SSL and Config().USE_SSL == "true":
            ssl_ctx = ssl.create_default_context(cafile=Config().CA_CERT_PATH)
            ssl_ctx.check_hostname = (
                False  # set True if hostname verification is required
            )
            ssl_ctx.verify_mode = ssl.CERT_REQUIRED
            args["ssl"] = ssl_ctx

        return args

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(
            (
                f"mysql+aiomysql://{Config().MYSQL_USER}:{Config().MYSQL_PASSWORD}"
                f"@{Config().MYSQL_HOST}/{Config().MYSQL_DATABASE}?charset=utf8mb4"
            ),
            connect_args=self._build_connect_args(),
            pool_size=constants.DB_POOL_SIZE,
            max_overflow=constants.DB_MAX_OVERFLOW,
            pool_timeout=constants.DB_POOL_TIMEOUT,
            pool_recycle=constants.DB_POOL_RECYCLE,
            pool_pre_ping=constants.DB_POOL_PRE_PING,
            isolation_level=constants.DB_ISOLATION_LEVEL,
            echo=False,
            future=True,
        )

    def get_engine(self) -> AsyncEngine:
        """
        Return the singleton SQLAlchemy Engine instance.

        Why this pattern:
        - Engine creation is relatively expensive (establishes connection pool, dialect setup).
        - We only need ONE Engine per process; sessions are lightweight and derived from it.
        - Multiple threads (e.g., concurrent FastAPI requests during cold start) may call
          get_engine() simultaneously. Without a lock, each could create its own Engine,
          leading to:
            * Duplicate pools (wasted connections)
            * Inconsistent configuration
            * Higher startup latency

        Concurrency control:
        - First a fast path check (if _engine_instance is already initialized) to avoid
          acquiring the lock on every call (cheap common case).
        - Then a lock is acquired only if the Engine is still None (slow path).
        - Inside the lock we check again (double-checked locking) to ensure another thread
          didn't already create it while we were waiting.

        Result:
        - Thread-safe lazy initialization
        - Minimal synchronization overhead after initialization
        """
        global _engine_instance

        # Fast path: already initialized
        if BaseDB._engine_instance is not None:
            return BaseDB._engine_instance

        # Slow path: guard initialization so only one thread creates the Engine
        with BaseDB._engine_lock:
            if (
                BaseDB._engine_instance is None
            ):  # Re-check inside lock (double-checked locking)
                BaseDB._engine_instance = self._create_engine()

        return BaseDB._engine_instance

    async def dispose_engine(self) -> None:
        """
        Dispose the async engine (e.g., on application shutdown) to close all pooled connections.
        """
        if BaseDB._engine_instance is not None:
            await BaseDB._engine_instance.dispose()
