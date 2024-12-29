import logging
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional

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


class MpvPlayer(VideoPlayer):
    """Video player using mpv."""

    def __init__(self, extra_args: Optional[List[str]] = None) -> None:
        """Initializes the player."""
        self.extra_args = extra_args or []
        self._check_mpv_installed()

    @staticmethod
    def _check_mpv_installed() -> None:
        """Checks if fzf is installed."""
        try:
            logger.debug("Перевірка встановлення mpv.")
            subprocess.run(["mpv", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            logger.error("mpv не встановлено!")
            raise

    def play(self, urls: List[str]) -> None:
        """
        Plays video from the specified URLs using mpv.

        Args:
            urls: List of video URLs.
        """
        if not urls:
            logger.error("Посилання на відео відсутні.")
            return

        try:
            logger.info(f"Відтворення {len(urls)} епізодів через mpv")
            logger.debug(f"Додаткові аргументи: {self.extra_args}")
            logger.debug(f"Посилання: {urls}")

            command = ["mpv"] + self.extra_args + urls
            subprocess.run(command, capture_output=True, check=True)
        except FileNotFoundError:
            logger.error("Плеєр mpv не встановлено!")
        except subprocess.SubprocessError as error:
            logger.error(f"Помилка запуску mpv: {error}")
