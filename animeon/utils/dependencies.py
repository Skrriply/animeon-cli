import logging
import subprocess

logger = logging.getLogger(__name__)

DEPENDENCIES = {
    "mpv": ["mpv", "--version"],
    "fzf": ["fzf", "--version"],
    "bash": ["bash", "--version"],
    "jq": ["jq", "--version"],
    "chafa": ["chafa", "--version"],
    "kitty": ["kitty", "--version"],
}


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
            logger.warning(f"{name} is not installed!")
