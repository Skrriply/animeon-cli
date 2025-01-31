import logging
from pathlib import Path
from typing import Optional

from animeon.constants import CACHE_DIR
from animeon.core import HTTPClient

logger = logging.getLogger(__name__)


class ImageDownloader:
    """Downloads and optionally caches images."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initializes the class.

        Args:
            http_client: HTTP client for making requests.
        """
        self.http_client = http_client
        self.cache_dir = CACHE_DIR / "posters"

    def download_image(self, image_url: str) -> Optional[Path]:
        """
        Downloads an image from a URL.

        Args:
            image_url: URL of the image to download.

        Returns:
            Path to the downloaded image or None if the image could not be downloaded.
        """
        logger.debug(f"Downloading image from URL: {image_url}")

        filename = image_url.rsplit("/", maxsplit=1)[-1]
        image_path = self.cache_dir / filename
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        if image_path.exists():
            logger.debug(f"Image found in cache: {image_path}")
            return image_path

        image = self.http_client.get(image_url)

        if not image:
            return None

        with open(image_path, "wb") as file:
            file.write(image.content)
        logger.debug(f"Image saved at: {image_path}")

        return image_path
