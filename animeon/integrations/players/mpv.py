import logging
import subprocess
from typing import List, Optional

from .base import BasePlayer

logger = logging.getLogger(__name__)


class MpvPlayer(BasePlayer):
    """A class to interact with the mpv video player."""

    EXECUTABLE = "mpv"

    def __init__(self, extra_args: Optional[List[str]] = None) -> None:
        """
        Initializes the class.

        Args:
            extra_args: Optional list of extra arguments to pass to mpv.
        """
        self.extra_args = extra_args

    def _build_command(self, url: str, title: Optional[str] = None) -> List[str]:
        """
        Builds the mpv command.

        Args:
            url: The video URL to play.
            title: Optional title of the video to display in mpv.

        Returns:
            The built command.
        """
        command = [self.EXECUTABLE]

        # Adds title if provided
        if title:
            command.append(f"--title={title}")

        # Adds extra args if provided
        if self.extra_args:
            command.extend(self.extra_args)

        # Adds URL
        command.append(url)

        return command

    def play(self, url: str, title: Optional[str] = None) -> None:
        """
        Plays video from the specified URL.

        Args:
            url: The video URL to play.
            title: Optional title of the video to display in mpv.
        """
        logger.info(f"Playing episode via mpv: {url}")

        command = self._build_command(url, title)

        logger.debug(f"Executing command: {' '.join(command)}")

        try:
            with subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                process.communicate()
        except FileNotFoundError:
            logger.error("Mpv not found. Please install it and try again")
            return
        except subprocess.SubprocessError as error:
            logger.error(f"Mpv failed: {error}")
            return
