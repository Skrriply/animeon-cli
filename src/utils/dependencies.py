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
            with subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                process.communicate()
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error(f"{name} is not installed!")
