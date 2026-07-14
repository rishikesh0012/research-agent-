"""Production startup script with health checks."""

import sys
import asyncio
from pathlib import Path

from app.config import settings
from app.utils.logging import logger
from app.main import app


async def health_check():
    """
    Perform startup health checks.
    """
    checks_passed = 0
    checks_total = 0
    
    # Check 1: Configuration validation
    checks_total += 1
    try:
        settings.validate()
        logger.info("✓ Configuration validation passed")
        checks_passed += 1
    except ValueError as e:
        logger.error(f"✗ Configuration validation failed: {e}")
    
    # Check 2: API keys present
    checks_total += 1
    if settings.openai_api_key and settings.tavily_api_key:
        logger.info("✓ API keys configured")
        checks_passed += 1
    else:
        logger.error("✗ Missing API keys")
    
    # Check 3: Log directory writable
    checks_total += 1
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        test_file = log_dir / ".test"
        test_file.touch()
        test_file.unlink()
        logger.info("✓ Log directory writable")
        checks_passed += 1
    except Exception as e:
        logger.warning(f"✗ Log directory check failed: {e}")
    
    # Summary
    logger.info(f"\nHealth check: {checks_passed}/{checks_total} passed")
    return checks_passed == checks_total


async def startup():
    """
    Perform startup sequence.
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Run health checks
    if not await health_check():
        logger.error("Health check failed - exiting")
        sys.exit(1)
    
    logger.info("✓ Startup complete - ready to serve")


if __name__ == "__main__":
    asyncio.run(startup())
