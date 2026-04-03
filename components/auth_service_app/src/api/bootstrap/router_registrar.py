from fastapi import FastAPI

from src.api.controllers import auth_router, health_router, role_router, user_router


class RouterRegistrar:
    """Handles registration of all FastAPI routers."""

    @staticmethod
    def register(app: FastAPI):
        """Registers routers with the FastAPI application."""
        app.include_router(health_router)
        app.include_router(auth_router)
        app.include_router(role_router)
        app.include_router(user_router)
