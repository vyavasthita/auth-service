from fastapi import FastAPI
from api.controllers import HealthController, AuthController


class RouterRegistrar:
    """
    Handles registration of all FastAPI routers for the application.
    """
    @staticmethod
    def register(app: FastAPI):
        # Register health check router
        app.include_router(HealthController().router)
        app.include_router(AuthController().router)