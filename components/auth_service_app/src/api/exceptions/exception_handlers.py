"""Centralized registration of FastAPI exception handlers for the API."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.api.exceptions.token_exception import InvalidTokenException
from src.api.exceptions.user_exception import (
    EmailFormatException,
    InvalidCredentialsException,
    PhoneNumberAlreadyExistsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def register_exception_handlers(app: FastAPI):
    """Register all custom and built-in exception handlers to the FastAPI app."""

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_exception_handler(
        request: Request,
        exc: UserAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(EmailFormatException)
    async def email_format_exception_handler(
        request: Request,
        exc: EmailFormatException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(PhoneNumberAlreadyExistsException)
    async def phone_number_already_exists_exception_handler(
        request: Request,
        exc: PhoneNumberAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
        request: Request,
        exc: InvalidTokenException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error."},
        )
