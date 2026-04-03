from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import DatabaseDependency
from src.api.dtos.user_dto import UserMeResponseDTO
from src.api.exceptions import InvalidTokenException
from src.api.models import User
from src.api.services import AuthService, AuthServiceImpl
from src.utils import AuthServiceLogger

logger = AuthServiceLogger.get_logger()

user_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@user_router.get(
    "/me",
    response_model=UserMeResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    user_id: str,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
    access_token: str | None = Cookie(default=None),
) -> UserMeResponseDTO:
    """Return the authenticated user's details."""
    if not access_token:
        raise InvalidTokenException()

    user: User = await auth_service.validate_token(
        db_session=db_session,
        token=access_token,
        user_id=UUID(user_id).bytes,
    )

    return UserMeResponseDTO(
        user_id=str(UUID(bytes=user.user_id)),
        username=user.username,
        created_at=str(user.created_at),
    )
