import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, List

from animeon.models import Anime, AnimePreview

from .formatter import Formatter
from .image_downloader import ImageDownloader

logger = logging.getLogger(__name__)


class AnimePreviewGenerator:
    """Generates anime previews in JSON format."""

    def __init__(
        self, text_formatter: Formatter, image_downloader: ImageDownloader
    ) -> None:
        """
        Initializes the class.

        Args:
            text_formatter: Object for formatting anime text previews.
            image_downloader: Object for downloading anime images.
        """
        self.text_formatter = text_formatter
        self.image_downloader = image_downloader

    def _generate_preview_data(self, anime: Anime) -> AnimePreview:
        """
        Generates preview data for a single anime.

        Args:
            anime: Anime to generate preview data for.

        Returns:
            Preview data for the anime.
        """
        text_preview = self.text_formatter.format(anime)
        poster_path = ""

        if self.image_downloader and anime.poster:
            image_path = self.image_downloader.download_image(anime.poster)
            if image_path:
                poster_path = str(image_path)

        return AnimePreview(text_content=text_preview, poster_path=poster_path)

    def generate(self, anime_list: List[Anime]) -> Path:
        """
        Generates previews for a list of anime.

        Args:
            anime_list: List of anime to generate previews for.

        Returns:
            Path to the generated previews file.
        """
        logger.info(f"Generating previews for {len(anime_list)} anime")
        previews = {
            anime.title: self._generate_preview_data(anime).to_dict()
            for anime in anime_list
        }

        return self._save_to_temp_file(previews)

    def _save_to_temp_file(self, previews: Dict) -> Path:
        """
        Saves the previews to a temporary JSON file.
        
        Args:
            previews: Previews to save.

        Returns:
            Path to the temporary JSON file.
        """
        logger.debug("Creating temporary JSON file")
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", delete=False
        ) as preview_file:
            json.dump(previews, preview_file, ensure_ascii=False, indent=4)
            preview_file_path = Path(preview_file.name)
            logger.debug(f"Created temporary file at: {preview_file_path}")
        return preview_file_path
