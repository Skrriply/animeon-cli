import logging

from animeon.config import LOG_COLORS, LOG_DATE_FORMAT, LOG_FORMAT, LOG_LEVEL, LOG_RESET


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds color to log messages."""

    def __init__(self) -> None:
        """Initializes the formatter."""
        super().__init__(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color.

        Args:
            record: Log record to format.

        Returns:
            Formatted log message.
        """
        color = LOG_COLORS.get(record.levelno, LOG_RESET)
        record.levelname = f"{color}{record.levelname}{LOG_RESET}"

        return super().format(record)


class LoggerManager:
    """Manages logging setup and configuration."""

    def __init__(self) -> None:
        """Initializes the class."""
        self.root_logger = logging.getLogger()
        self.logger = logging.getLogger(__name__)

    def _create_console_handler(self) -> logging.Handler:
        """
        Creates and configures console handler.

        Returns:
            Configured console handler.
        """
        handler = logging.StreamHandler()
        formatter = ColorFormatter()
        handler.setFormatter(formatter)

        return handler

    def _clear_handlers(self) -> None:
        """Removes existing handlers from root logger."""
        self.root_logger.handlers.clear()

    def setup_logging(self) -> None:
        """Sets up basic logging configuration."""
        self._clear_handlers()
        self.root_logger.setLevel(LOG_LEVEL)
        handler = self._create_console_handler()
        self.root_logger.addHandler(handler)
        self.logger.info("Logging started")

    def enable_debug(self) -> None:
        """Enables debug level logging."""
        self.root_logger.setLevel(logging.DEBUG)
        self.logger.debug("Debug logging enabled")
