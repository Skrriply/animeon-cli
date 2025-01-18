import logging
from typing import Any, Dict, List, Optional

from animeon.models import Anime, Episode, Fandub, Player, SearchResult

logger = logging.getLogger(__name__)


class Extractor:
    """Class for extracting data from API responses."""

    def _get_poster_url(
        self, poster_endpoint: str, poster_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Gets the URL of the poster image.

        Args:
            poster_endpoint: The base URL for posters.
            poster_data: Data for the poster image.

        Returns:
            URL of the poster image if successful, None otherwise.
        """
        filename = poster_data.get("original") or poster_data.get("preview")

        if not filename:
            logger.warning("Poster not found")
            return None

        return f"{poster_endpoint}/{filename}"

    def extract_search_result(self, data: Dict[str, Any]) -> Optional[SearchResult]:
        """
        Extracts search result data from the API response.

        Args:
            data: API response data.

        Returns:
            SearchResult object if successful, None otherwise.
        """
        anime_id = data.get("id")
        if not anime_id:
            logger.warning("Anime ID not found")
            return None

        anime_title = data.get("titleUa")
        if not anime_title:
            logger.warning("Anime title not found")
            return None

        return SearchResult(id_=anime_id, title=anime_title)

    def extract_anime(
        self, poster_endpoint: str, data: Dict[str, Any]
    ) -> Optional[Anime]:
        """
        Extracts anime data from the API response.

        Args:
            poster_endpoint: The base URL for posters.
            data: API response data.

        Returns:
            Anime object if successful, None otherwise.
        """
        anime_id = data.get("id")
        if not anime_id:
            logger.warning("Anime ID not found")
            return None

        title = data.get("titleUa")
        if not title:
            logger.warning("Anime title not found")
            return None

        return Anime(
            id_=anime_id,
            title=title,
            poster=self._get_poster_url(poster_endpoint, data.get("image", {})),
            rating=data.get("malScored"),
            scored_by=data.get("malScoredBy"),
            type_=data.get("type"),
            episodes=data.get("episodes"),
            episodes_aired=data.get("episodesAired"),
            status=data.get("status"),
            genres=[
                genre.get("nameUa")
                for genre in data.get("genres", [])
                if "nameUa" in genre
            ],
            studio=data.get("studio", {}).get("name"),
            release_year=data.get("releaseDate"),
            episode_duration=data.get("episodeTime"),
            producer=data.get("producer"),
            description=data.get("description"),
            mal_id=data.get("malId"),
        )

    def extract_players(self, data: Dict[str, Any]) -> List[Player]:
        """
        Extracts player data from the API response.

        Args:
            data: API response data.

        Returns:
            List of Player objects if successful, empty list otherwise.
        """
        players_data = data.get("player", [])

        players = []
        for player_item in players_data:
            player_id = player_item.get("id")
            if not player_id:
                logger.warning("Player ID not found")
                continue

            player_name = player_item.get("name")
            if not player_name:
                logger.warning("Player name not found")
                continue

            players.append(Player(id_=player_id, name=player_name))

        return players

    def extract_fandub(self, data: Dict[str, Any]) -> Optional[Fandub]:
        """
        Extracts fandub data from the API response.

        Args:
            data: API response data.

        Returns:
            Fandub object if successful, None otherwise.
        """
        fandub_data = data.get("fundub", {})

        fandub_id = fandub_data.get("id")
        if not fandub_id:
            logger.warning("Fandub ID not found")
            return None

        fandub_name = fandub_data.get("name")
        if not fandub_name:
            logger.warning("Fandub name not found")
            return None

        return Fandub(
            id_=fandub_id,
            name=fandub_name,
            players=self.extract_players(data),
        )

    def extract_episode(self, data: Dict[str, Any]) -> Optional[Episode]:
        """
        Extracts episode data from the API response.

        Args:
            data: API response data.

        Returns:
            Episode object if successful, None otherwise.
        """
        episode_id = data.get("id")
        if not episode_id:
            logger.warning("Episode ID not found")
            return None

        episode = data.get("episode")
        if not episode:
            logger.warning("Episode not found")
            return None

        return Episode(id_=episode_id, episode=episode)
