"""
J.A.R.V.I.S — Configuration Management
=======================================
Centralized configuration with validation and type safety.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class APIKeys(BaseModel):
    """API keys for external services."""
    openrouter: Optional[str] = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY"))
    wolfram: Optional[str] = Field(default_factory=lambda: os.getenv("WOLFRAM_APP_ID"))
    openweather: Optional[str] = Field(default_factory=lambda: os.getenv("OPENWEATHER_API_KEY"))

    @validator('*', pre=True)
    def empty_string_to_none(cls, v):
        """Convert empty strings to None."""
        if v == "":
            return None
        return v


class ServerConfig(BaseModel):
    """Server configuration."""
    host: str = Field("localhost", env="JARVIS_HOST")
    port: int = Field(8765, env="JARVIS_PORT")
    debug: bool = Field(False, env="JARVIS_DEBUG")
    reload: bool = Field(False, env="JARVIS_RELOAD")


class ExternalServiceConfig(BaseModel):
    """Configuration for external services."""
    # Timeouts in seconds
    http_timeout: int = Field(15, env="JARVIS_HTTP_TIMEOUT")
    wolfram_timeout: int = Field(10, env="JARVIS_WOLFRAM_TIMEOUT")
    weather_timeout: int = Field(8, env="JARVIS_WEATHER_TIMEOUT")
    search_timeout: int = Field(8, env="JARVIS_SEARCH_TIMEOUT")

    # Retry configuration
    max_retries: int = Field(3, env="JARVIS_MAX_RETRIES")
    base_delay: float = Field(1.0, env="JARVIS_BASE_DELAY")
    max_delay: float = Field(10.0, env="JARVIS_MAX_DELAY")

    # Circuit breaker configuration
    failure_threshold: int = Field(5, env="JARVIS_FAILURE_THRESHOLD")
    recovery_timeout: int = Field(30, env="JARVIS_RECOVERY_TIMEOUT")


class JarvisConfig(BaseModel):
    """Main application configuration."""
    api_keys: APIKeys = Field(default_factory=APIKeys)
    server: ServerConfig = Field(default_factory=ServerConfig)
    external_services: ExternalServiceConfig = Field(
        default_factory=ExternalServiceConfig
    )

    # Feature flags
    demo_mode: bool = Field(False, env="JARVIS_DEMO_MODE")
    enable_metrics: bool = Field(True, env="JARVIS_ENABLE_METRICS")
    enable_health_checks: bool = Field(True, env="JARVIS_ENABLE_HEALTH_CHECKS")

    # Default city for weather
    default_city: str = Field("New York", env="JARVIS_CITY")

    # OpenRouter model (Claude via OpenRouter)
    openrouter_model: str = Field("anthropic/claude-sonnet-4", env="OPENROUTER_MODEL")

    def validate_config(self) -> bool:
        """Validate the configuration and return True if valid."""
        try:
            # Additional validation logic can go here
            # For now, basic validation is handled by Pydantic
            return True
        except Exception:
            return False

    class Config:
        # Allow extra attributes for flexibility
        extra = "ignore"
        # Use environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global configuration instance
_config: Optional[JarvisConfig] = None


def get_config() -> JarvisConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = JarvisConfig()
    return _config


def reload_config() -> JarvisConfig:
    """Reload configuration from environment and .env file."""
    global _config
    _config = JarvisConfig()
    return _config


def validate_config() -> bool:
    """Validate the current configuration and return True if valid."""
    try:
        config = get_config()
        # Additional validation logic can go here
        return True
    except Exception:
        return False