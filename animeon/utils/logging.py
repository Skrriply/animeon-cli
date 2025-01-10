import logging
from typing import Optional

from animeon.config import LoggingConfig


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds color to log messages."""

    def __init__(self, config: Optional[LoggingConfig] = None) -> None:
        """Initializes the formatter.

        Args:
            config: Optional logging configuration. If not provided, default configuration will be used.
        """
        self.config = config or LoggingConfig.default()
        super().__init__(fmt=self.config.format, datefmt=self.config.date_format)

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color.

        Args:
            record: Log record to format.

        Returns:
            Formatted log message.
        """
        color = self.config.colors.get(record.levelno, self.config.reset)
        record.levelname = f"{color}{record.levelname}{self.config.reset}"

        return super().format(record)


class LoggerManager:
    """Manages logging setup and configuration."""

    def __init__(self, config: Optional[LoggingConfig] = None) -> None:
        """
        Initializes the class.

        Args:
            config: Optional logging configuration. If not provided, default configuration will be used.
        """
        self.config = config or LoggingConfig.default()
        self.root_logger = logging.getLogger()
        self.logger = logging.getLogger(__name__)

    def _create_console_handler(self) -> logging.Handler:
        """
        Creates and configures console handler.

        Returns:
            Configured console handler.
        """
        handler = logging.StreamHandler()
        formatter = ColorFormatter(self.config)
        handler.setFormatter(formatter)

        return handler

    def _clear_handlers(self) -> None:
        """Removes existing handlers from root logger."""
        self.root_logger.handlers.clear()

    def setup_logging(self) -> None:
        """Sets up basic logging configuration."""
        self._clear_handlers()
        self.root_logger.setLevel(self.config.level)
        handler = self._create_console_handler()
        self.root_logger.addHandler(handler)
        self.logger.info("Logging started")

    def enable_debug(self) -> None:
        """Enables debug level logging."""
        self.root_logger.setLevel(logging.DEBUG)
        self.logger.debug("Debug logging enabled")
