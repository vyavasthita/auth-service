from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils import AuthServiceLogger
from src.api.dtos import (
    RegisterUserRequestDTO,
    RegisterUserResponseDTO,
    LoginUserRequestDTO,
    LoginUserResponseDTO,
    ValidateTokenRequestDTO,
    ValidateTokenResponseDTO,
)
from src.api.models import User
from src.api.dependencies import DatabaseDependency
from src.api.services import AuthService, AuthServiceImpl


class AuthController:
    def __init__(self):
        self.router = APIRouter(tags=["Auth"])
        self.logger = AuthServiceLogger.get_logger()
        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/validate-token",
            self.validate_token,
            methods=["POST"],
        )

    async def register(
        self,
        request: RegisterUserRequestDTO,
        db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
        auth_service: AuthService = Depends(AuthServiceImpl),
    ) -> RegisterUserResponseDTO:
        """Register a new user."""
        self.logger.info(f"Register endpoint called for email: {request.email}")
        user: User = await auth_service.register(
            db_session=db_session,
            email=request.email,
            name=request.name,
            password=request.password,
            phone_number=request.phone_number,
        )
        self.logger.info(f"User registered: {user.email}")
        return RegisterUserResponseDTO(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
        )

    async def login(
        self,
        request: LoginUserRequestDTO,
        db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
        auth_service: AuthService = Depends(AuthServiceImpl),
    ) -> LoginUserResponseDTO:
        """Authenticate a user and return an access token."""
        self.logger.info(f"Login endpoint called for email: {request.email}")
        token: str = await auth_service.login(
            db_session=db_session,
            email=request.email,
            password=request.password,
        )
        self.logger.info(f"User logged in: {request.email}")
        return LoginUserResponseDTO(access_token=token)

    async def validate_token(
        self,
        request: ValidateTokenRequestDTO,
        db_session: AsyncSession = Depends(DatabaseDependency.get_db_session),
        auth_service: AuthService = Depends(AuthServiceImpl),
    ) -> ValidateTokenResponseDTO:
        """Validate a JWT token and return claims if valid."""
        user: User = await auth_service.validate_token(
            db_session=db_session, token=request.token
        )
        return ValidateTokenResponseDTO(email=user.email, message="Token is valid.")
