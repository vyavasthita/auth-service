
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import AuthServiceLogger
from api.dtos import (
    RegisterUserRequestDTO,
    RegisterUserResponseDTO,
    LoginUserRequestDTO,
    LoginUserResponseDTO,
)
from api.models import User
from api.dependencies import get_db_session
from api.services import AuthService, AuthServiceImpl


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

    async def register(
        self,
        request: RegisterUserRequestDTO,
        db_session: AsyncSession = Depends(get_db_session),
        auth_service: AuthService = Depends(AuthServiceImpl),
    ) -> RegisterUserResponseDTO:
        self.logger.info(f"Register endpoint called for email: {request.email}")
        user: User = await auth_service.register(
            db_session=db_session,
            name=request.name,
            email=request.email,
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
        db_session: AsyncSession = Depends(get_db_session),
        auth_service: AuthService = Depends(AuthServiceImpl),
    ) -> LoginUserResponseDTO:
        self.logger.info(f"Login endpoint called for email: {request.email}")
        token: str = await auth_service.login(
            db_session,
            email=request.email,
            password=request.password,
        )
        self.logger.info(f"User logged in: {request.email}")
        return LoginUserResponseDTO(access_token=token)