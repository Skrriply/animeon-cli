import logging
import subprocess
from abc import ABC, abstractmethod
from typing import List

logger = logging.getLogger(__name__)


class VideoPlayer(ABC):
    """Abstract class for video player."""

    @abstractmethod
    def play(self, urls: List[str]) -> None:
        """
        Plays video from the specified URLs.

        Args:
            urls: List of video URLs.
        """
        pass

    @staticmethod
    def _validate_urls(urls: List[str]) -> bool:
        """
        Validates URLs.

        Args:
            urls: List of video URLs.

        Returns:
            True if URLs are valid, False otherwise.
        """
        if not urls:
            logger.error("Video URLs are missing!")
            return False
        return True


class MpvPlayer(VideoPlayer):
    """Video player using mpv."""

    def play(self, urls: List[str]) -> None:
        """
        Plays video from the specified URLs using mpv.

        Args:
            urls: List of video URLs.
        """
        self._validate_urls(urls)

        try:
            logger.info(f"Playing {len(urls)} episodes via mpv")
            logger.debug(f"URLs: {urls}")

            command = ["mpv", *urls]
            with subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                process.communicate()
        except subprocess.SubprocessError as error:
            logger.error(f"Error executing mpv: {error}")
