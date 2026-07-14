"""Production deployment configuration."""

import logging
from app.config import settings
from app.utils.logging import setup_logging

# Setup production logging
logger = setup_logging(
    log_level=settings.log_level,
    log_file="logs/production.log"
)

# Production-specific settings
if settings.debug:
    logger.warning("DEBUG mode is enabled - disable for production")

logger.info(
    f"Production environment initialized - {settings.app_name} v{settings.app_version}"
)
logger.info(f"Using NVIDIA API with model: {settings.nvidia_model}")
logger.info(f"API Endpoint: {settings.nvidia_base_url}")
