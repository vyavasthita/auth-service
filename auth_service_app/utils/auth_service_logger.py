import logging
from threading import Lock
from api.dependencies import Config


class AuthServiceLogger:
    """
    Singleton logger for the Auth Service. Use AuthServiceLogger.get_logger() to get the logger instance.
    """
    _instance = None
    _lock = Lock()

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger = logging.getLogger(Config().OTEL_SERVICE_NAME)
                    logger.setLevel(Config().LOG_LEVEL)
                    # Ensure logs propagate to root logger (so Loki/sidecar can capture)
                    logger.propagate = True
                    # Optionally, do not add a handler if running in containerized/cloud env
                    # to avoid duplicate logs. Only add if no handlers and not root.
                    if not logger.handlers and logger.name != "root":
                        handler = logging.StreamHandler()
                        formatter = logging.Formatter(
                            "%(asctime)s %(levelname)s [%(name)s] %(message)s"
                        )
                        handler.setFormatter(formatter)
                        logger.addHandler(handler)
                    cls._instance = logger
        return cls._instance
