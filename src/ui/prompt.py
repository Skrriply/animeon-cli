import logging
import subprocess
from typing import List, Optional, Set

from src.config import FZF_DEFAULT_COMMAND, JQ_DEFAULT_COMMAND

logger = logging.getLogger(__name__)


class Prompt:
    """Class for prompting user with fzf."""

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
            logger.warning("No options available for selection")
            return False
        return True

    def single_select(
        self, prompt_text: str, options: List[str], preview_file: Optional[str] = None
    ) -> Optional[str]:
        """
        Prompts user to select one option.

        Args:
            prompt_text: Input prompt text.
            options: List of options.

        Returns:
            Selected option or None if no option is selected.
        """
        if not self._validate_options(options):
            return None

        # Changes input prompt text
        command = [*FZF_DEFAULT_COMMAND, "--prompt", prompt_text]

        # Adds preview if preview file is provided
        if preview_file:
            preview_command = f"{' '.join(JQ_DEFAULT_COMMAND)} --arg title {{}} '.[$title]' {preview_file}"
            command.extend(["--preview", preview_command])

        return self._run_fzf(command, "\n".join(options))

    def multi_select(self, prompt_text: str, options: List[str]) -> Optional[Set[str]]:
        """
        Prompts user to select multiple options.

        Args:
            prompt_text: Input prompt text.
            options: List of options.

        Returns:
            Set of selected options or None if no option is selected.
        """
        if not self._validate_options(options):
            return None

        # Changes input prompt text and enables multiselection
        command = [*FZF_DEFAULT_COMMAND, "--prompt", prompt_text, "--multi"]

        stdout = self._run_fzf(command, "\n".join(options))

        if not stdout:
            return None

        return set(stdout.split("\n"))

    def _run_fzf(self, command: List[str], input_: str) -> Optional[str]:
        """
        Runs fzf with the specified command and input.

        Args:
            command: Command to run fzf.
            input_: Input for fzf.

        Returns:
            Selected option(s) as string or None if no selection was made or error occurred.
        """
        try:
            with subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:
                stdout, _ = process.communicate(input=input_)

                return stdout.strip() if stdout else None
        except subprocess.CalledProcessError as error:
            if error.returncode == 130:
                logger.info("User didn't select anything")
            else:
                logger.error(f"Error executing fzf: {error}")

            return None
