import logging
import subprocess
from typing import List, Optional, Set

logger = logging.getLogger(__name__)


class Prompt:
    """Class for prompting user with fzf."""

    FZF_BASE_COMMAND = ["fzf", "--reverse", "--cycle"]

    def __init__(self) -> None:
        """Initializes the class."""
        self._check_fzf_installed()

    @staticmethod
    def _check_fzf_installed() -> None:
        """Checks if fzf is installed."""
        try:
            logger.debug("Перевірка встановлення fzf.")
            subprocess.run(["fzf", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            logger.error("fzf не встановлено!")
            raise

    @staticmethod
    def _validate_options(options: List[str]) -> bool:
        """
        Validates options.

        Args:
            options: List of options.

        Returns:
            True if options are valid, False otherwise.
        """
        if not options:
            logger.warning("Немає доступних опцій для вибору")
            return False
        return True

    def single_select(self, prompt_text: str, options: List[str]) -> Optional[str]:
        """
        Prompts user to select one option.

        Args:
            prompt_text: Prompt text.
            options: List of options.

        Returns:
            Selected option or None if no option is selected.
        """
        if not self._validate_options(options):
            return None

        command = self.FZF_BASE_COMMAND + ["--prompt", prompt_text]

        return self._run_fzf(command, "\n".join(options))

    def multi_select(self, prompt_text: str, options: List[str]) -> Optional[Set[str]]:
        """
        Prompts user to select multiple options.

        Args:
            prompt_text: Prompt text.
            options: List of options.

        Returns:
            Set of selected options or None if no option is selected.
        """
        if not self._validate_options(options):
            return None

        command = self.FZF_BASE_COMMAND + ["--prompt", prompt_text, "--multi"]

        stdout = self._run_fzf(command, "\n".join(options))

        if not stdout:
            return None

        return set(stdout.split("\n"))

    def _run_fzf(self, command: List[str], input_: str) -> Optional[str]:
        """
        Runs fzf with the specified command and input.

        Args:
            fzf_command: Command to run fzf.
            input_: Input for fzf.

        Returns:
            Selected option(s) as string or None if no selection was made or error occurred.
        """
        try:
            process = subprocess.run(
                command,
                input=input_,
                capture_output=True,
                text=True,
                check=True,
            )

            if not process.stdout:
                return None

            return process.stdout.strip()
        except subprocess.CalledProcessError:
            logger.error("Помилка при виконанні fzf")
            return None
