import logging
from typing import Any, Dict, List, Optional

from src.models import Anime, Episode, Fandub, Player
from src.utils import build_url, normalize_query

from .http import HTTPClient

logger = logging.getLogger(__name__)


class AnimeAPI:
    """Client for interacting with AnimeOn API."""

    BASE_URL = "https://animeon.club"

    def __init__(self) -> None:
        """Initializes AnimeOn client."""
        self.http_client = HTTPClient()
        self._headers = {"Referer": self.BASE_URL}

    def _get_data(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> Optional[Any]:
        """
        Makes a GET request to the API and returns the response data.

        Args:
            endpoint: API endpoint.
            params: Optional query parameters.

        Returns:
            Response data if successful, None otherwise
        """
        url = build_url(self.BASE_URL, endpoint)

        logger.debug(f"Виконується GET запит до {url} з параметрами: {params}")
        return self.http_client.get(url, params=params, headers=self._headers)

    def search(self, query: str) -> Optional[List[Anime]]:
        """
        Searches for anime by query.

        Args:
            query: Search query.

        Returns:
            List of Anime objects if successful, None otherwise.
        """
        encoded_query = normalize_query(query)

        if not encoded_query:
            logger.error("Запит порожній або містить заборонені символи.")
            return None

        endpoint = f"api/anime/search/{encoded_query}"
        params = {"full": "false"}

        data = self._get_data(endpoint, params)

        if not data or "result" not in data:
            logger.error("Запит повернув неправильні дані.")
            return None

        return [
            Anime(
                item["id"],
                int(item["malId"]),
                item["titleUa"].strip(),
            )
            for item in data["result"]
        ]

    def get_episodes(self, player_id: int, fandub_id: int) -> Optional[List[Episode]]:
        """
        Gets episodes for the specified player and fandub.

        Args:
            player_id: Player ID.
            fandub_id: Fandub ID.

        Returns:
            List of Episode objects if successful, None otherwise.
        """
        endpoint = f"api/player/episodes/{player_id}/{fandub_id}"
        data = self._get_data(endpoint)

        if not data:
            logger.error("Запит повернув неправильні дані.")
            return None

        return [Episode(item["id"], item["episode"]) for item in data]

    def get_video_url(self, episode_id: int) -> Optional[str]:
        """
        Gets video URL for the specified episode.

        Args:
            episode_id: Episode ID.

        Returns:
            Video URL if successful, None otherwise.
        """
        endpoint = f"api/player/episode/{episode_id}"
        data = self._get_data(endpoint)

        if not data or "videoUrl" not in data:
            logger.error("Запит повернув неправильні дані.")
            return None

        return data["videoUrl"]

    def get_fandubs_and_players(self, anime_id: int) -> Optional[List[Fandub]]:
        """
        Gets available fandubs and players for the specified anime.

        Args:
            anime_id: Anime ID.

        Returns:
            List of Fandub objects if successful, None otherwise
        """
        endpoint = f"api/player/fundubs/{anime_id}"
        data = self._get_data(endpoint)

        if not data:
            logger.error("Запит повернув неправильні дані.")
            return None

        return [
            Fandub(
                item["fundub"]["id"],
                item["fundub"]["name"],
                [
                    Player(
                        player["id"],
                        player["name"],
                    )
                    for player in item.get("player", [])
                ],
            )
            for item in data
        ]
