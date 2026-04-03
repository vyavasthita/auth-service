from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import DatabaseDependency
from src.api.dtos import (
    LoginUserRequestDTO,
    LoginUserResponseDTO,
    RegisterUserRequestDTO,
    RegisterUserResponseDTO,
    ValidateTokenRequestDTO,
    ValidateTokenResponseDTO,
)
from src.api.models import User
from src.api.services import AuthService, AuthServiceImpl
from src.utils import AuthServiceLogger

logger = AuthServiceLogger.get_logger()


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
    logger.info(f"Register endpoint called for email: {request.email}")
    user: User = await auth_service.register(
        db_session=db_session,
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        password=request.password,
        phone_number=request.phone_number,
    )
    logger.info(f"User registered: {user.email}")
    return RegisterUserResponseDTO(
        email=user.email,
        first_name=user.profile.first_name,
        last_name=user.profile.last_name,
        phone_number=user.profile.phone_number,
    )


@auth_router.post(
    "/login",
    response_model=LoginUserResponseDTO,
)
async def login(
    request: LoginUserRequestDTO,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
) -> LoginUserResponseDTO:
    """Authenticate a user and return an access token."""
    logger.info(f"Login endpoint called for email: {request.email}")
    token: str = await auth_service.login(
        db_session=db_session,
        email=request.email,
        password=request.password,
    )
    logger.info(f"User logged in: {request.email}")
    return LoginUserResponseDTO(access_token=token)


@auth_router.post(
    "/validate",
    response_model=ValidateTokenResponseDTO,
)
async def validate_token(
    request: ValidateTokenRequestDTO,
    db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
    auth_service: AuthService = Depends(AuthServiceImpl),
) -> ValidateTokenResponseDTO:
    """Validate a JWT token and return claims if valid."""
    user: User = await auth_service.validate_token(db_session=db_session, token=request.token)
    return ValidateTokenResponseDTO(user_id=user.user_id, email=user.email, message="Token is valid.")
