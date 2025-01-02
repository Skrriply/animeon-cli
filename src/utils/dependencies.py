import logging
import subprocess

from src.config import DEPENDENCIES

logger = logging.getLogger(__name__)


def check_dependencies() -> None:
    """Checks all required dependencies."""
    logger.debug("Checking dependencies...")

    for name, command in DEPENDENCIES.items():
        try:
            logger.debug(f"Checking if {name} is installed")
            subprocess.run(command, capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error(f"{name} is not installed!")
