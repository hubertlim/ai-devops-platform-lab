"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    app_env: str = "development"
    app_name: str = "ai-devops-platform-lab"
    app_version: str = "0.1.0"

    api_host: str = "0.0.0.0"  # noqa: S104
    api_port: int = 8000
    api_log_level: str = "info"

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # AI Provider
    ai_provider: str = "mock"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    # Observability
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "ai-platform-api"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
