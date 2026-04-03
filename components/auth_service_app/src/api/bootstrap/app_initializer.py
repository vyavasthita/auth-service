from fastapi import FastAPI

from src.api.bootstrap.cors_registrar import CORSRegistrar
from src.api.bootstrap.instrumentation_setup import InstrumentationSetup
from src.api.bootstrap.router_registrar import RouterRegistrar
from src.api.exceptions import register_exception_handlers


class AppInitializer:
    """Orchestrates all initialization steps for the API application."""

    def pre_initialization(self):
        """Perform setup steps before FastAPI app instantiation."""
        pass

    def post_initialization(self, app: FastAPI):
        """Perform all setup steps that require the FastAPI app instance."""
        CORSRegistrar.register(app)
        register_exception_handlers(app)
        InstrumentationSetup.setup(app)
        RouterRegistrar.register(app)
