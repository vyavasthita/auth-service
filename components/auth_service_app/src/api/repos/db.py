from threading import Lock
import logging
import ssl
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.api.dependencies.config_dependency import Config
from src.utils.auth_service_logger import AuthServiceLogger


class DatabaseEngine:
    _engine_lock = Lock()
    _engine_instance: AsyncEngine | None = None
    _logger = AuthServiceLogger.get_logger()

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @logger.setter
    def logger(self, value: logging.Logger):
        self._logger = value

    def _build_connect_args(self):
        config = Config()
        args = {"connect_timeout": config.CONNECT_TIMEOUT}

        if config.USE_SSL and config.USE_SSL == "true":
            ssl_ctx = ssl.create_default_context(cafile=config.CA_CERT_PATH)
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_REQUIRED
            args["ssl"] = ssl_ctx

        return args

    def _create_engine(self) -> AsyncEngine:
        config = Config()
        self.logger.info(
            "Creating SQLAlchemy async engine: "
            f"pool_size={config.DB_POOL_SIZE}, "
            f"max_overflow={config.DB_MAX_OVERFLOW}, "
            f"pool_timeout={config.DB_POOL_TIMEOUT}, "
            f"pool_recycle={config.DB_POOL_RECYCLE}, "
            f"pool_pre_ping={config.DB_POOL_PRE_PING}, "
            f"isolation_level='{config.DB_ISOLATION_LEVEL}'"
        )

        return create_async_engine(
            (
                f"mysql+aiomysql://{quote_plus(config.MYSQL_USER)}:{quote_plus(config.MYSQL_PASSWORD)}"
                f"@{config.MYSQL_HOST}/{config.MYSQL_DATABASE}?charset=utf8mb4"
            ),
            connect_args=self._build_connect_args(),
            pool_size=config.DB_POOL_SIZE,
            max_overflow=config.DB_MAX_OVERFLOW,
            pool_timeout=config.DB_POOL_TIMEOUT,
            pool_recycle=config.DB_POOL_RECYCLE,
            pool_pre_ping=config.DB_POOL_PRE_PING,
            isolation_level=config.DB_ISOLATION_LEVEL,
            echo=False,
        )

    def get_engine(self) -> AsyncEngine:
        """
        Return the singleton SQLAlchemy Engine instance.
        Thread-safe lazy initialization with double-checked locking.
        """
        if DatabaseEngine._engine_instance is not None:
            return DatabaseEngine._engine_instance

        with DatabaseEngine._engine_lock:
            if DatabaseEngine._engine_instance is None:
                DatabaseEngine._engine_instance = self._create_engine()

        return DatabaseEngine._engine_instance

    async def dispose_engine(self) -> None:
        """Dispose the async engine on application shutdown."""
        with DatabaseEngine._engine_lock:
            if DatabaseEngine._engine_instance is not None:
                await DatabaseEngine._engine_instance.dispose()
                DatabaseEngine._engine_instance = None
