# app/utils/logger.py

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

def get_logger(name: str = 'flask_app') -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (default: 'flask_app')
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)

def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Optional logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Set default log file if none provided
    if log_file is None:
        log_file = log_dir / "app.log"

    # Determine log level (default to INFO if not specified or invalid)
    numeric_level = getattr(logging, (log_level or os.getenv("LOG_LEVEL", "INFO")).upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Setup file handler
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Get root logger
    root_logger = logging.getLogger()
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Set log level
    root_logger.setLevel(numeric_level)

    # Create logger for the application
    logger = logging.getLogger('flask_app')
    logger.info(f"Logging setup completed. Level: {logging.getLevelName(numeric_level)}")