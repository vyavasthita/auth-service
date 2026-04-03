from fastapi import APIRouter, Depends
from instrumentation_hub_fastapi import rate_limited_log

from src.api.dependencies import DatabaseDependency
from src.api.dependencies.config_dependency import Config
from src.utils import AuthServiceLogger

logger = AuthServiceLogger.get_logger()

health_router = APIRouter(
    prefix="",
    tags=["Health"],
)


@health_router.get(
    "/health",
    dependencies=[Depends(DatabaseDependency())],
)
@rate_limited_log(interval_seconds=Config().RATE_LIMITED_LOG_INTERVAL_SECONDS)
async def health_check() -> str:
    """Database connectivity check."""
    message = f"{Config().SERVICE_NAME} is healthy."

    if health_check._can_log:
        logger.info(message)
        
    return message
