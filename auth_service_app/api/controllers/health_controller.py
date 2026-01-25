from fastapi import APIRouter, Depends
from instrumentation_hub_fastapi import rate_limited_log
from api.utils import AuthServiceLogger
from api.dependencies.db_dependency import ValidateDBConnection
from api.dependencies.config_dependency import Config


class HealthController:
    def __init__(self):
        """
        Initialize the HealthController with API routes for health checks and a logger.
        """
        self.router = APIRouter(tags=["Health Check"])
        self.router.add_api_route(
            "/app_health",
            self.health_check,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/db_health",
            self.db_health_check,
            methods=["GET"],
            dependencies=[Depends(ValidateDBConnection())],
        )
        self.logger = AuthServiceLogger.get_logger()

    @rate_limited_log(interval_seconds=Config().RATE_LIMITED_LOG_INTERVAL_SECONDS)
    async def health_check(self) -> str:
        """
        Health check endpoint for the application.

        Returns:
            str: A message indicating the application is healthy.
        """
        message = f"{Config().OTEL_SERVICE_NAME} is healthy."
        if self.health_check._can_log:
            self.logger.info(message)
        return message

    async def db_health_check(self) -> str:
        """
        Health check endpoint for the database connection.

        Returns:
            str: A message indicating the database health status.
        """
        return "Hello from Auth Service DB Health Check"
