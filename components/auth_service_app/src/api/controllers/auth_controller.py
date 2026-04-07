from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import DatabaseDependency
from src.api.dependencies.config_dependency import Config
from src.api.dtos import (
    LoginUserRequestDTO,
    LoginUserResponseDTO,
    LogoutRequestDTO,
    RegisterUserRequestDTO,
    RegisterUserResponseDTO,
    ValidateTokenResponseDTO,
)
from src.api.exceptions import InvalidTokenException
from src.api.models import User
from src.api.services import AuthService, AuthServiceImpl
from src.utils import AuthServiceLogger

logger = AuthServiceLogger.get_logger()

config = Config()

auth_router = APIRouter(
    prefix="",
    tags=["Auth"],
)


@auth_router.post(
    "/register",
    response_model=RegisterUserResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterUserRequestDTO,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
) -> RegisterUserResponseDTO:
    """Register a new user."""
    logger.info(f"Register endpoint called for username: {request.username}")

    user: User = await auth_service.register(
        db_session=db_session,
        username=request.username,
        password=request.password,
    )
    logger.info(f"User registered: {user.username}")

    return RegisterUserResponseDTO(
        username=user.username,
    )


@auth_router.post(
    "/login",
    response_model=LoginUserResponseDTO,
)
async def login(
    request: LoginUserRequestDTO,
    response: Response,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
) -> LoginUserResponseDTO:
    """Authenticate a user and set an access token cookie."""
    logger.info(f"Login endpoint called for username: {request.username}")

    token, user_id = await auth_service.login(
        db_session=db_session,
        username=request.username,
        password=request.password,
    )

    response.set_cookie(
        key=config.COOKIE_NAME,
        value=token,
        httponly=config.COOKIE_HTTPONLY,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        path=config.COOKIE_PATH,
        max_age=config.TOKEN_EXPIRE_MINUTES * 60,
    )
    logger.info(f"User logged in: {request.username}")
    return LoginUserResponseDTO(user_id=str(UUID(bytes=user_id)))


@auth_router.post(
    "/validate",
    response_model=ValidateTokenResponseDTO,
    include_in_schema=False,
)
async def validate_token(
    user_id: str,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
    access_token: str | None = Cookie(default=None),
) -> ValidateTokenResponseDTO:
    """Validate a JWT token from the cookie and return claims if valid."""
    if not access_token:
        raise InvalidTokenException()

    user: User = await auth_service.validate_token(
        db_session=db_session,
        token=access_token,
        user_id=UUID(user_id).bytes,
    )

    return ValidateTokenResponseDTO(
        user_id=str(UUID(bytes=user.user_id)),
        username=user.username,
        message="Token is valid.",
    )


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    request: LogoutRequestDTO,
    response: Response,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
) -> dict:
    """Invalidate the session and clear the access token cookie."""
    await auth_service.logout(
        db_session=db_session,
        token=request.token,
        user_id=UUID(request.user_id).bytes,
    )

    response.delete_cookie(
        key=config.COOKIE_NAME,
        httponly=config.COOKIE_HTTPONLY,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        path=config.COOKIE_PATH,
    )
    return {"message": "Logged out successfully."}
