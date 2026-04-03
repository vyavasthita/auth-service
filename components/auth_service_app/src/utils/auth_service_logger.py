import logging
from threading import Lock

from src.api.dependencies.config_dependency import Config


class AuthServiceLogger:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the singleton logger instance for the Auth Service."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger = logging.getLogger(Config().SERVICE_NAME)
                    logger.setLevel(Config().LOG_LEVEL)
                    logger.propagate = True
                    if not logger.handlers and logger.name != "root":
                        handler = logging.StreamHandler()
                        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
                        handler.setFormatter(formatter)
                        logger.addHandler(handler)
                    cls._instance = logger
        return cls._instance
