from fastapi import APIRouter, Depends
from instrumentation_hub_fastapi import rate_limited_log
from src.utils import AuthServiceLogger
from src.api.dependencies import DatabaseDependency
from src.api.dependencies.config_dependency import Config


logger = AuthServiceLogger.get_logger()

health_router = APIRouter(
    prefix="",
    tags=["Health Check"],
)


@health_router.get("/app_health")
@rate_limited_log(interval_seconds=Config().RATE_LIMITED_LOG_INTERVAL_SECONDS)
async def health_check() -> str:
    message = f"{Config().OTEL_SERVICE_NAME} is healthy."
    if health_check._can_log:
        logger.info(message)
    return message


@health_router.get(
    "/db_health",
    dependencies=[Depends(DatabaseDependency())],
)
async def db_health_check() -> str:
    return "Hello from Auth Service DB Health Check"
