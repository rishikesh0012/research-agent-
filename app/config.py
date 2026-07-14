"""
Configuration module for the Enterprise Research Agent.
Manages environment variables, API keys, and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # NVIDIA API Configuration
    nvidia_api_key: str = os.getenv("NVIDIA_API_KEY", "")
    nvidia_model: str = os.getenv("NVIDIA_MODEL", "meta/llama-2-70b-chat")
    nvidia_base_url: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    nvidia_temperature: float = 0.7

    # Tavily Search Configuration
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    tavily_max_results: int = 10

    # Application Configuration
    app_name: str = "Enterprise Research Agent"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # LangSmith Configuration (Optional)
    langsmith_enabled: bool = os.getenv("LANGSMITH_ENABLED", "false").lower() == "true"
    langsmith_api_key: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    langsmith_project: Optional[str] = os.getenv("LANGSMITH_PROJECT")

    # Execution Configuration
    max_retries: int = 2
    execution_timeout_seconds: int = 300
    max_research_depth: int = 5

    # FastAPI Configuration
    fastapi_host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT", "8000"))
    fastapi_reload: bool = os.getenv("FASTAPI_RELOAD", "true").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate(self) -> None:
        """Validate critical configuration settings."""
        if not self.nvidia_api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")
        if not self.tavily_api_key:
            print("WARNING: TAVILY_API_KEY not set. Search tool disabled.")


# Global settings instance
settings = Settings()
