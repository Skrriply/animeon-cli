import logging
from typing import Any, Dict, List, Optional

from animeon.models import Anime, Episode, Fandub, SearchResult

from .extractor import Extractor
from .http import HTTPClient

logger = logging.getLogger(__name__)


class AnimeOnAPI:
    """Client for interacting with AnimeOn API."""

    BASE_URL = "https://animeon.club"
    _HEADERS = {"Referer": BASE_URL}
    _SEARCH_ENDPOINT = f"{BASE_URL}/api/anime"
    _ANIME_ENDPOINT = f"{BASE_URL}/api/anime"
    _FANDUBS_ENDPOINT = f"{BASE_URL}/api/player/fundubs"
    _EPISODES_ENDPOINT = f"{BASE_URL}/api/player/episodes"
    _EPISODE_ENDPOINT = f"{BASE_URL}/api/player/episode"
    _POSTER_ENDPOINT = f"{BASE_URL}/api/uploads/images"

    def __init__(
        self,
        http_client: HTTPClient,
        extractor: Extractor,
        timeout: Optional[int] = None,
    ) -> None:
        """
        Initializes the class.

        Args:
            http_client: HTTP client for making requests.
            extractor: Extractor for parsing API responses.
            timeout: Optional timeout for HTTP requests.
        """
        self.http_client = http_client
        self.extractor = extractor
        self.timeout = timeout

    def _make_request(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """
        Makes a GET request to the specified URL.

        Args:
            url: URL to make the request to.
            params: Optional parameters to include in the request.

        Returns:
            JSON response data if successful, None otherwise.
        """
        try:
            response = self.http_client.get(
                url, params=params, headers=self._HEADERS, timeout=self.timeout
            )
            return response.json() if response else None
        except ValueError as error:
            logger.error(f"Error parsing JSON: {error}")
            return None

    def search(self, query: str) -> List[SearchResult]:
        """
        Searches for anime by query.

        Args:
            query: Search query.

        Returns:
            List of SearchResult objects if successfull, empty list otherwise.
        """
        logger.info(f"Searching anime with query: {query}")

        params = {
            "pageSize": 16,
            "search": query,
        }
        data = self._make_request(self._SEARCH_ENDPOINT, params)

        if not data:
            logger.error(f'Search for "{query}" returned no data')
            return []

        return [
            result
            for item in data.get("results", [])
            if (result := self.extractor.extract_search_result(item))
        ]

    def get_anime(self, anime_id: int) -> Optional[Anime]:
        """
        Gets anime data by ID.

        Args:
            anime_id: Anime ID.

        Returns:
            Anime object if successful, None otherwise.
        """
        url = f"{self._ANIME_ENDPOINT}/{anime_id}"
        data = self._make_request(url)

        if not data:
            logger.error(f"Failed to retrieve anime data for ID: {anime_id}")
            return None

        return self.extractor.extract_anime(self._POSTER_ENDPOINT, data)

    def get_fandubs_and_players(self, anime_id: int) -> List[Fandub]:
        """
        Gets available fandubs and players for the specified anime.

        Args:
            anime_id: Anime ID.

        Returns:
            List of Fandub objects if successful, empty list otherwise
        """
        url = f"{self._FANDUBS_ENDPOINT}/{anime_id}"
        data = self._make_request(url)

        if not data:
            logger.error(f"No fandubs found for anime ID: {anime_id}")
            return []

        return [
            fandub for item in data if (fandub := self.extractor.extract_fandub(item))
        ]

    def get_episodes(self, player_id: int, fandub_id: int) -> List[Episode]:
        """
        Gets episodes for the specified player and fandub.

        Args:
            player_id: Player ID.
            fandub_id: Fandub ID.

        Returns:
            List of Episode objects if successful, empty list otherwise.
        """
        url = f"{self._EPISODES_ENDPOINT}/{player_id}/{fandub_id}"
        data = self._make_request(url)

        if not data:
            logger.error(
                f"No episodes found for player ID {player_id} and fandub ID {fandub_id}"
            )
            return []

        return [
            episode
            for item in data
            if (episode := self.extractor.extract_episode(item))
        ]

    def get_video_url(self, episode_id: int) -> Optional[str]:
        """
        Gets video URL for the specified episode.

        Args:
            episode_id: Episode ID.

        Returns:
            Video URL if successful, None otherwise.
        """
        url = f"{self._EPISODE_ENDPOINT}/{episode_id}"
        data = self._make_request(url)

        if not data:
            logger.error(f"Failed to retrieve video URL for episode ID {episode_id}")
            return None

        return data.get("videoUrl")
