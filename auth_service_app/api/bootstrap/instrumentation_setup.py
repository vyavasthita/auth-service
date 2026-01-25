from fastapi import FastAPI
from instrumentation_hub_fastapi import FastAPIInstrumentation
from instrumentation_hub_fastapi.middlewares.api_instrumentation import (
    InstrumentationSanitizationConfig, InstrumentationConfigFactory, MetricType
)
from api.dependencies import Config


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
            sensitive_fields={'password', 'token', 'api_key', 'ssn', 'phone_number'},
            max_field_length=64
        )
    
    @staticmethod
    def setup(app: FastAPI):
        """
        Set up instrumentation for the FastAPI application.

        This may include tracing, metrics, and logging configuration.

        Args:
            app (FastAPI): The FastAPI application to instrument.
        """
        FastAPIInstrumentation().setup(
            app,
            metrics_config=InstrumentationSetup._get_metrics_config(),
            sanitization_config=InstrumentationSetup._get_sanitization_config(),
            service_name=Config().OTEL_SERVICE_NAME,
            log_level=Config().LOG_LEVEL
        )