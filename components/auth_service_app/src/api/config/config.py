from src.api.config.app_config import AppSettings
from src.api.config.cors_config import CORSSettings
from src.api.config.db_pool_config import DBPoolSettings
from src.api.config.jwt_config import JWTSettings
from src.api.config.mysql_config import MySQLSettings
from src.api.config.observability_config import ObservabilitySettings
from src.api.config.open_api_config import OpenAPISettings


class Settings(
    CORSSettings,
    OpenAPISettings,
    AppSettings,
    MySQLSettings,
    DBPoolSettings,
    JWTSettings,
    ObservabilitySettings,
):
    """Application settings, composed from multiple config classes."""

    pass
