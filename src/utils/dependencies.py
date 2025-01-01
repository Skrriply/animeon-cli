import logging
import subprocess

from src.config import DEPENDENCIES

logger = logging.getLogger(__name__)


def check_dependencies() -> None:
    """Checks all required dependencies."""
    logger.debug("Перевірка залежностей...")

    for name, command in DEPENDENCIES.items():
        try:
            logger.debug(f"Перевірка встановлення {name}.")
            subprocess.run(command, capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error(f"{name} не встановлено!")
