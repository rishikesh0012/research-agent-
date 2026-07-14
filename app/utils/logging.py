"""
Structured logging configuration for the Enterprise Research Agent.
Provides Rich-formatted console logging and optional file logging.
"""

import logging
import sys
from typing import Optional
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console
from app.config import settings


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure structured logging with Rich formatting.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("enterprise_research_agent")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create console handler with Rich formatting
    console = Console(file=sys.stdout, force_terminal=True)
    handler = RichHandler(console=console, show_time=True, show_level=True, show_path=True)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Optional file handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logging(log_level=settings.log_level)
