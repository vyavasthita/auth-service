import secrets
from functools import wraps
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import generate_auth_token, hash_password, verify_password
from api.exceptions import (
    InvalidCredentialsException,
)
from api.models import User
from api.repositories import AuthRepository, AuthRepositoryImpl
from .auth_service import AuthService


class AuthServiceImpl(AuthService):

    def __init__(
        self,
        auth_repository: AuthRepository = Depends(AuthRepositoryImpl),
    ):
        super().__init__(auth_repository)
    
    @AuthService.is_new_user
    async def register(
        self,
        db_session: AsyncSession,
        name: str,
        email: str,
        password: str,
        phone_number: str,
    ) -> User:
        user = User()

        user.id = uuid4().bytes
        user.name = name
        user.email = email
        user.password = hash_password(password)
        user.phone_number = phone_number

        return await self.auth_repository.save(db_session, user)

    @AuthService.is_valid_user
    async def login(
        self,
        db_session: AsyncSession,  # Automatically passed to the is_valid_user decorator
        email: str,  # Automatically passed to the is_valid_user decorator
        password: str,
        user: User,  # Filled by the is_valid_user decorator
    ) -> str:
        if not verify_password(password, user.password):
            raise InvalidCredentialsException()
        
        return generate_auth_token()