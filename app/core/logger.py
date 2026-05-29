"""Custom Logger Configuration"""

import logging
import sys
from typing import Optional


class AppLogger:
    """
    Simple logger for the application.
    Logs messages with timestamps and levels.
    """

    def __init__(self, name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create console handler if no handlers exist
        if not self.logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level.upper()))

            # Create formater
            # Create formater
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(extra_info)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def _log(self, level: int, msg: str, request_id: Optional[str] = None, **kwargs):
        """Internal log method with extra fields"""
        extra = {"extra_info": {}}

        if request_id:
            extra["extra_info"]["request_id"] = request_id

        if kwargs:
            extra["extra_info"].update(kwargs)

        # Convert extra dict to string for logging
        extra_str = ", ".join([f"{k}={v}" for k, v in extra["extra_info"].items()])
        extra["extra_info"] = extra_str  # type: ignore

        self.logger.log(level, msg, extra=extra)

    def info(self, msg: str, request_id: Optional[str] = None, **kwargs):
        """Log INFO level message"""
        self._log(logging.INFO, msg, request_id, **kwargs)

    def error(self, msg: str, request_id: Optional[str] = None, **kwargs):
        """Log ERROR level message"""
        self._log(logging.ERROR, msg, request_id, **kwargs)

    def warning(self, msg: str, request_id: Optional[str] = None, **kwargs):
        """Log WARNING level message"""
        self._log(logging.WARNING, msg, request_id, **kwargs)

    def debug(self, msg: str, request_id: Optional[str] = None, **kwargs):
        """Log DEBUG level message"""
        self._log(logging.DEBUG, msg, request_id, **kwargs)


# Create a default logger instance
default_logger = AppLogger("app")
