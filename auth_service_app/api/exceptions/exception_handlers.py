"""Centralized registration of FastAPI exception handlers for the API."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    EmailFormatException,
)


def register_exception_handlers(app: FastAPI):
    # Handle custom user already exists exception
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
    
    # Handle FastAPI HTTPException
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    # Fallback for unhandled exceptions
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error."},
        )
