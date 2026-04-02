from pydantic_settings import BaseSettings


class ObservabilitySettings(BaseSettings):
    """OpenTelemetry observability settings."""

    OTEL_SERVICE_NAME: str = "auth-service"
    LOGGING_BACKEND: str = "opensearch"
    TRACING_BACKEND: str = "tempo"
    METRICS_BACKEND: str = "prometheus"
    RATE_LIMITED_LOG_INTERVAL_SECONDS: int = 60
