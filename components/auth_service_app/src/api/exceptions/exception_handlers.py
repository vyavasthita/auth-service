"""Centralized registration of FastAPI exception handlers for the API."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.api.exceptions.user_exception import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    EmailFormatException,
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
