import logging
from typing import Optional

from animeon.constants import ANIME_STATUSES, ANIME_TYPES
from animeon.models import Anime

logger = logging.getLogger(__name__)


class Formatter:
    """Formats anime information into a text preview."""

    def __init__(self) -> None:
        """Initializes the class."""
        self.unknown_value = "Невідомо"
        self.no_rating_value = "Немає"

        # It will be formatted with a bash script
        self.separator_tag = "{separator}"

    def format(self, anime: Anime) -> str:
        """
        Formats anime information into a text preview.

        Args:
            anime: Anime to format.

        Returns:
            Formatted text preview.
        """
        logger.debug(f"Formatting text preview for: {anime.title}")

        type_ = ANIME_TYPES.get(anime.type_) if anime.type_ else self.unknown_value
        rating = self._format_rating(anime.rating, anime.scored_by)
        status = (
            ANIME_STATUSES.get(anime.status) if anime.status else self.unknown_value
        )
        genres = ", ".join(anime.genres) if anime.genres else self.unknown_value

        return (
            f"{self.separator_tag}\n"
            f"{anime.title}\n"
            f"{self.separator_tag}\n"
            f"⭐ Рейтинг:     {rating}\n"
            f"🎬 Тип:         {type_}\n"
            f"🗂️ Епізоди:     {anime.episodes_aired or '?'} / {anime.episodes or '?'}\n"
            f"📊 Статус:      {status}\n"
            f"📚 Жанри:       {genres}\n"
            f"🗓️ Рік:         {anime.release_year or self.unknown_value}\n"
            f"📺 Студія:      {anime.studio or self.unknown_value}\n"
            f"👤 Режисер:     {anime.producer or self.unknown_value}\n"
            f"⏳ Тривалість:  {anime.episode_duration or self.unknown_value}\n"
            f"{self.separator_tag}\n"
            "📝 Опис:\n"
            f"{anime.description or self.unknown_value}"
        )

    def _format_rating(self, rating: Optional[float], scored_by: Optional[int]) -> str:
        """
        Formats the rating of an anime.

        Args:
            rating: Rating of the anime.
            scored_by: Number of people who scored the rating.

        Returns:
            Formatted rating.
        """
        if rating:
            return f"{rating} ({scored_by or '???'} голосів)"
        return self.no_rating_value
