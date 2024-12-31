import logging

from src.config import LOG_COLORS, LOG_DATE_FORMAT, LOG_FORMAT, LOG_RESET


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds color to log messages."""

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color.

        Args:
            record: Log record to format.

        Returns:
            Formatted log message.
        """
        levelname_color = LOG_COLORS.get(record.levelno, LOG_RESET)
        record.levelname = f"{levelname_color}{record.levelname}{LOG_RESET}"

        return super().format(record)


def setup_logging() -> None:
    """Configures logging.

    Args:
        debug: Enable debug logging
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Removes existing handlers
    root_logger.handlers.clear()

    # Adds colored console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ColorFormatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    )
    root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.info("Логування розпочато.")
