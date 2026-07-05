"""
utils/logger.py
Configures logging to file and standard output for debugging and auditing.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOGS_DIR

def setup_logger(name: str = "toolkit") -> logging.Logger:
    """
    Sets up a logger with a rotating file handler and standard output stream.
    
    Args:
        name (str): Name of the logger.
        
    Returns:
        logging.Logger: The configured Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Log Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s:%(lineNo)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Stream Handler (console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        # File Handler (rotating)
        log_file = LOGS_DIR / "app.log"
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Single shareable logger instance
logger = setup_logger()
