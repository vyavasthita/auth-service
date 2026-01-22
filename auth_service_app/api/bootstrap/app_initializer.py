from fastapi import FastAPI
from api.bootstrap import InstrumentationSetup, CORSRegistrar, RouterRegistrar
from api.exceptions import register_exception_handlers

class AppInitializer:
    """
    Orchestrates all initialization steps for the API application.
    Delegates instrumentation and router setup to dedicated classes.
    """
    def pre_initialization(self):
        """
        Perform setup steps that must occur before FastAPI app instantiation.
        (No-op for primitive param API, but placeholder for future use.)
        """
        pass

    def post_initialization(self, app: FastAPI):
        """
        Perform all setup steps that require the FastAPI app instance.
        """
        # Add CORS middleware using modular registrar
        CORSRegistrar.register(app)

        # Register exception handlers
        
        register_exception_handlers(app)

        # Set up observability (tracing, metrics, logging)
        InstrumentationSetup.setup(app)

        # Register routers
        RouterRegistrar.register(app)
