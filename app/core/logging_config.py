"""Logging Configuration"""

import logging
import logging.config
import sys

from app.core.config import settings


def setup_logging():
    """Setup logging configuration for the entire application"""

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "detailed",
                "level": logging.DEBUG if settings.debug else logging.INFO,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "detailed",
                "level": logging.INFO,
            },
        },
        "root": {
            "level": logging.DEBUG if settings.debug else logging.INFO,
            "handlers": ["console", "file"],
        },
    }

    logging.config.dictConfig(log_config)
