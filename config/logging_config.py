import logging
import logging.handlers
from pathlib import Path
import os

def setup_logging(log_dir='logs', log_level=logging.INFO):
    """Configure logging with rotation and different handlers"""
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers = []

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    # File Handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / 'scraper.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(detailed_formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # Error File Handler
    error_handler = logging.handlers.RotatingFileHandler(
        log_path / 'error.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    # Set up specific loggers for different components
    loggers = {
        'scraper': logging.getLogger('scraper'),
        'middleware': logging.getLogger('middleware'),
        'storage': logging.getLogger('storage'),
        'extractor': logging.getLogger('extractor')
    }

    # Configure component-specific settings if needed
    for name, component_logger in loggers.items():
        component_logger.setLevel(log_level)

    return loggers

def get_logger(name):
    """Get a logger for a specific component"""
    return logging.getLogger(name)

# Optional: Add specific logging configurations for different environments
def setup_development_logging():
    return setup_logging(log_level=logging.DEBUG)

def setup_production_logging():
    return setup_logging(log_level=logging.INFO)
