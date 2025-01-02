import logging
import subprocess
from abc import ABC, abstractmethod
from typing import List

from src.config import MPV_DEFAULT_COMMAND

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
            formatted_urls = "\n- ".join(urls)
            logger.info(f"Playing {len(urls)} episodes via mpv")
            logger.debug(f"URLs: {formatted_urls}")

            command = MPV_DEFAULT_COMMAND + urls
            subprocess.run(command, capture_output=True, check=True)
        except subprocess.CalledProcessError as error:
            logger.error(f"Error executing mpv: {error}")
