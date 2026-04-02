from fastapi import FastAPI
from src.api.controllers import HealthController, AuthController


class RouterRegistrar:
    """Handles registration of all FastAPI routers."""

    @staticmethod
    def register(app: FastAPI):
        """Registers routers with the FastAPI application."""
        app.include_router(HealthController().router)
        app.include_router(AuthController().router)
