# TODO: Split classes into separate files
import logging
from typing import Optional

import colorama


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds color to log messages."""

    # Color codes for log messages and reset
    COLORS = {
        logging.DEBUG: colorama.Fore.CYAN,
        logging.INFO: colorama.Fore.GREEN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.MAGENTA,
    }
    RESET = colorama.Style.RESET_ALL

    def __init__(
        self, format: Optional[str] = None, date_format: Optional[str] = None
    ) -> None:
        """
        Initializes the class.

        Args:
            format: Format string to use.
            date_format: Date format string to use.
        """
        super().__init__(fmt=format, datefmt=date_format)

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color.

        Args:
            record: Log record to format.

        Returns:
            Formatted log message.
        """
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        return super().format(record)


class LoggerManager:
    """Manages logging setup and configuration."""

    def __init__(
        self,
        level: str,
        format: Optional[str] = None,
        date_format: Optional[str] = None,
    ) -> None:
        """
        Initializes the class.

        Args:
            level: Logging level to use.
        """
        self.level = level
        self.format = format
        self.date_format = date_format
        self.root_logger = logging.getLogger()
        self.logger = logging.getLogger(__name__)

    def _create_console_handler(self) -> logging.Handler:
        """
        Creates and configures console handler.

        Returns:
            Configured console handler.
        """
        handler = logging.StreamHandler()
        formatter = ColorFormatter(format=self.format, date_format=self.date_format)
        handler.setFormatter(formatter)

        return handler

    def _clear_handlers(self) -> None:
        """Removes existing handlers from root logger."""
        self.root_logger.handlers.clear()

    def setup_logging(self) -> None:
        """Sets up basic logging configuration."""
        self._clear_handlers()
        self.root_logger.setLevel(self.level)
        handler = self._create_console_handler()
        self.root_logger.addHandler(handler)
        self.logger.info("Logging started")

    def enable_debug(self) -> None:
        """Enables debug level logging."""
        self.root_logger.setLevel(logging.DEBUG)
        self.logger.debug("Debug logging enabled")
