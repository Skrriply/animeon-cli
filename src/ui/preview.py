import json
import logging
import subprocess
import tempfile
from typing import List, Optional

from src.config import CHAFA_DEFAULT_COMMAND
from src.core import HTTPClient
from src.models import Anime

logger = logging.getLogger(__name__)


class AnimePreviewGenerator:
    """Class for creating previews of anime content."""

    TYPES = {
        "tv": "ТБ-серіал",
        "movie": "Фільм",
        "ova": "OVA",
        "ona": "ONA",
        "special": "Спешл",
    }
    STATUSES = {
        "ongoing": "Онґоінґ",
        "released": "Завершено",
        "anons": "Незабаром",
    }

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initializes the class.

        Args:
            http_client: HTTP client for making requests.
        """
        self.http_client = http_client

    def _create_preview(self, anime: Anime) -> str:
        """
        Creates a formatted preview string for an anime.

        Args:
            anime: Anime object to create preview.

        Returns:
            Formatted string.
        """
        logger.debug(f"Creating preview for anime: {anime.title}")

        poster = self._generate_image_preview(anime.poster)
        type_ = self.TYPES.get(anime.type_, "Невідомо")
        rating = (
            f"{anime.rating} ({anime.scored_by or '???'} голосів)"
            if anime.rating
            else "Немає"
        )
        status = self.STATUSES.get(anime.status, "Невідомо")
        separator = "─" * 50

        return (
            f"{poster}\n"
            f"{separator}\n"
            f"{anime.title}\n"
            f"{separator}\n"
            f"📺 Тип: {type_}\n"
            f"🎬 Епізодів: {anime.episodes_aired or '?'}/{anime.episodes or '?'}\n"
            f"⭐ Рейтинг: {rating}\n"
            f"📅 Рік: {anime.release_year or 'Невідомо'}\n"
            f"📊 Статус: {status}\n"
            f"🎬 Продюсер: {anime.producer or 'Невідомо'}\n"
            f"{separator}\n"
            "📝 Опис:\n"
            f"{anime.description or 'Опис відсутній'}"
        )

    def _generate_image_preview(self, image_url: str) -> Optional[str]:
        """
        Generates ASCII art preview of an image URL.

        Args:
            image_url: URL of the image to convert.

        Returns:
            ASCII art string if successful, None if failed.
        """
        logger.debug(f"Generating image preview for URL: {image_url}")

        try:
            image = self.http_client.get(image_url, as_json=False)

            with subprocess.Popen(
                CHAFA_DEFAULT_COMMAND,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) as process:
                stdout, _ = process.communicate(input=image)

                return stdout.decode().strip() if stdout else None
        except subprocess.CalledProcessError as error:
            logger.error(f"Error executing chafa: {error}")
            return None

    def generate(self, anime_list: List[Anime]) -> str:
        """
        Generates preview data for a list of anime.

        Args:
            anime_list: List of Anime objects to generate previews.

        Returns:
            Path to temporary JSON file containing preview data.
        """
        logger.info(f"Generating previews for {len(anime_list)} anime")

        previews = {}
        for anime in anime_list:
            previews[anime.title] = self._create_preview(anime)

        logger.debug("Creating temporary JSON file")

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", delete=False
        ) as preview_file:
            json.dump(previews, preview_file, ensure_ascii=False, indent=4)
            preview_file_path = preview_file.name
            logger.debug(f"Created temporary file at: {preview_file_path}")

        return preview_file_path
