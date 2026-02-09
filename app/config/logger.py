"""
Logging configuration for the Real Estate AI Platform.

Provides a simple logger factory that respects DEBUG settings.

Usage:
    from app.config.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Hello world")
"""
import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given module name.
    
    Args:
        name: Usually __name__ from the calling module
        
    Returns:
        Configured logging.Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  # Set level to INFO to show info and error
        
    return logger
