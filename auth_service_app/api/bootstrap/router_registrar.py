from fastapi import FastAPI
from api.controllers import HealthController, AuthController


class RouterRegistrar:
    """
    Handles registration of all FastAPI routers for the application.
    """
    @staticmethod
    def register(app: FastAPI):
        """
        Registers the given FastAPI application with the necessary routers.

        Args:
            app (FastAPI): The FastAPI application to register routers with.
        """
        # Register health check router
        app.include_router(HealthController().router)
        app.include_router(AuthController().router)