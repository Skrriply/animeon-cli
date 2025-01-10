import logging
from dataclasses import dataclass
from typing import Dict, Type

from .base import BaseConfig


@dataclass
class LoggingConfig(BaseConfig):
    """Logging configuration."""

    level: int
    format: str
    date_format: str
    colors: Dict[int, str]
    reset: str

    @classmethod
    def default(cls: Type["LoggingConfig"]) -> "LoggingConfig":
        """
        Creates default configuration.

        Args:
            cls: Class type.

        Returns:
            Default LogConfig instance.
        """
        return cls(
            level=logging.ERROR,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            date_format="%Y-%m-%d %H:%M:%S",
            colors={
                logging.DEBUG: "\033[0;36m",
                logging.INFO: "\033[0;32m",
                logging.WARNING: "\033[0;33m",
                logging.ERROR: "\033[0;31m",
                logging.CRITICAL: "\033[0;35m",
            },
            reset="\033[0m",
        )
