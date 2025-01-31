import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BasePlayer(ABC):
    """Abstract class for video players."""

    @abstractmethod
    def play(self, url: str) -> None:
        """
        Plays video from the specified URL.

        Args:
            url: The video URL to play.
        """
        pass
