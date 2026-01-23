from fastapi import FastAPI
from instrumentation_hub_fastapi import FastAPIInstrumentation
from instrumentation_hub_fastapi.middlewares.api_instrumentation import (
    InstrumentationSanitizationConfig, InstrumentationConfigFactory, MetricType
)

class InstrumentationSetup:
    """
    Handles OpenTelemetry logging, tracing, and metrics setup for FastAPI.
    """
    @staticmethod
    def _get_metrics_config():
        """
        Returns the InstrumentationConfigFactory for enabled metrics.
        """
        return InstrumentationConfigFactory(enabled_metrics=[
            MetricType.REQUEST_LATENCY,
            MetricType.ERROR_COUNT,
        ])

    @staticmethod
    def _get_sanitization_config():
        """
        Returns the InstrumentationSanitizationConfig for sensitive fields and max length.
        """
        return InstrumentationSanitizationConfig(
            sensitive_fields={'password', 'token', 'api_key', 'ssn'},
            max_field_length=64
        )
    
    @staticmethod
    def setup(app: FastAPI):
        """
        Set up instrumentation for FastAPI app with internal metrics and sanitization config.

        Args:
            app: FastAPI app instance
        """
        config = InstrumentationSetup._get_metrics_config()
        sanitization = InstrumentationSetup._get_sanitization_config()

        FastAPIInstrumentation().setup(app, metrics_config=config, sanitization_config=sanitization)