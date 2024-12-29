import logging

# Constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds color to log messages."""

    COLORS = {
        logging.DEBUG: "\033[0;36m",  # Cyan
        logging.INFO: "\033[0;32m",  # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",  # Red
        logging.CRITICAL: "\033[0;35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color.

        Args:
            record: Log record to format.

        Returns:
            Formatted log message.
        """
        levelname_color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{levelname_color}{record.levelname}{self.RESET}"

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
