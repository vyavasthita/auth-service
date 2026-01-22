from fastapi import FastAPI
from instrumentation_hub_fastapi import FastAPIInstrumentation


class InstrumentationSetup:
    """
    Handles OpenTelemetry logging, tracing, and metrics setup for FastAPI.
    """
    @staticmethod
    def setup(app: FastAPI):
        FastAPIInstrumentation().setup(app)