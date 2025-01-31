import logging
import subprocess
from typing import List, Optional

from animeon.constants import FZF_BASE_COMMAND

from .base import BasePrompter

logger = logging.getLogger(__name__)


class FzfPrompter(BasePrompter):
    """A class to interact with the fzf."""

    def __init__(self, extra_args: Optional[List[str]] = None) -> None:
        """
        Initializes the class.

        Args:
            extra_args: Optional list of extra arguments to pass to fzf.
        """
        self.extra_args = extra_args

    def _build_command(
        self, title: Optional[str] = None, preview_command: Optional[str] = None
    ) -> List[str]:
        """
        Builds the fzf command.

        Args:
            title: Optional title to display in fzf.
            preview_command: Optional preview command to use in fzf.

        Returns:
            The built command.
        """
        command = [*FZF_BASE_COMMAND]

        # Adds title if provided
        if title:
            command.extend(["--prompt", title])

        # Adds preview if preview command is provided
        if preview_command:
            command.extend(["--preview", preview_command])

        # Adds extra args if provided
        if self.extra_args:
            command.extend(self.extra_args)

        return command

    def _execute(self, command: List[str], input_: str) -> Optional[str]:
        """
        Executes the fzf command.

        Args:
            command: The command to execute.
            input_: The input to pass to fzf.

        Returns:
            The selected option, or None if no option was selected or if an error occurred.
        """
        logger.debug(f"Executing command: {' '.join(command)}")

        try:
            with subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:
                stdout, _ = process.communicate(input=input_)

                # Handles the case where fzf is closed by the user
                if process.returncode == 130:
                    logger.info("User didn't select anything from fzf")
                    return None

                if process.returncode != 0:
                    logger.error(f"Fzf failed with code {process.returncode}")
                    return None

                return stdout.strip() if stdout else None
        except FileNotFoundError:
            logger.error("Fzf not found. Please install it and try again")
            return None

    def prompt(
        self,
        options: List[str],
        title: Optional[str] = None,
        preview_command: Optional[str] = None,
    ) -> Optional[str]:
        """
        Prompts the user to select an option from a list of options.

        Args:
            options: A list of options to select from.
            title: Optional title to display in fzf.
            preview_command: Optional preview command to use in fzf.

        Returns:
            The selected option, or None if no option was selected or if an error occurred.
        """
        if not options:
            logger.info("No options available for selection")
            return None

        command = self._build_command(title, preview_command)

        return self._execute(command, "\n".join(options))
