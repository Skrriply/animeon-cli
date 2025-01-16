import logging
from dataclasses import dataclass
from typing import Dict, Type

from colorama import Fore, Style

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
                logging.DEBUG: Fore.CYAN,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.MAGENTA,
            },
            reset=Style.RESET_ALL,
        )
