import json
import logging
import subprocess
import tempfile
from typing import List, Optional

from animeon.constants import ANIME_STATUSES, ANIME_TYPES, CHAFA_BASE_COMMAND
from animeon.core import HTTPClient
from animeon.models import Anime

logger = logging.getLogger(__name__)


class AnimePreviewGenerator:
    """Class for creating previews of anime content."""

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

        poster = self._generate_image_preview(anime.poster) if anime.poster else ""
        type_ = ANIME_TYPES.get(anime.type_) if anime.type_ else "Невідомо"
        rating = (
            f"{anime.rating or '0.0'} ({anime.scored_by or '???'} голосів)"
            if anime.rating
            else "Немає"
        )
        status = ANIME_STATUSES.get(anime.status) if anime.status else "Невідомо"
        genres = ", ".join(anime.genres) if anime.genres else "Невідомо"
        separator = "─" * 50

        return (
            f"{poster}\n"
            f"{separator}\n"
            f"{anime.title}\n"
            f"{separator}\n"
            f"⭐ Рейтинг:     {rating}\n"
            f"🎬 Тип:         {type_}\n"
            f"🗂️ Епізоди:     {anime.episodes_aired or '?'}/{anime.episodes or '?'}\n"
            f"📊 Статус:      {status}\n"
            f"📚 Жанри:       {genres}\n"
            f"🗓️ Рік:         {anime.release_year or 'Невідомо'}\n"
            f"📺 Студія:      {anime.studio or 'Невідомо'}\n"
            f"👤 Режисер:     {anime.producer or 'Невідомо'}\n"
            f"⏳ Тривалість:  {anime.episode_duration or 'Невідомо'}\n"
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
            image = self.http_client.get(image_url)

            if image:
                with subprocess.Popen(
                    CHAFA_BASE_COMMAND,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ) as process:
                    stdout, _ = process.communicate(input=image.content)

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
