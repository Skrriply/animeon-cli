import logging
from typing import Any, Dict, List, Optional

from animeon.config import ApiConfig
from animeon.models import Anime, Episode, Fandub, Player
from animeon.utils import build_url, normalize_query

from .http import HTTPClient

logger = logging.getLogger(__name__)


class AnimeAPI:
    """Client for interacting with AnimeOn API."""

    BASE_URL = "https://animeon.club"
    HEADERS = {"Referer": BASE_URL}

    def __init__(
        self, http_client: HTTPClient, config: Optional[ApiConfig] = None
    ) -> None:
        """
        Initializes the class.

        Args:
            http_client: HTTP client for making requests.
            config: Optional API configuration. If not provided, default configuration will be used.
        """
        self.http_client = http_client
        self.config = config or ApiConfig.default()

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

        logger.debug(f"Making GET request to {url} with parameters: {params}")
        return self.http_client.get(url, params=params, headers=self.HEADERS, timeout=self.config.timeout)

    def _get_poster_url(self, poster: Optional[str]) -> str:
        """
        Builds URL for poster image.

        Args:
            poster: Poster image filename.

        Returns:
            URL for poster image if successful, empty string otherwise.
        """
        if not poster:
            logger.warning("Poster not found")
            return ""

        return build_url(self.BASE_URL, f"api/uploads/images/{poster}")

    def _parse_anime(self, data: Dict[str, Any]) -> Optional[Anime]:
        """
        Parses Anime data from the API response.

        Args:
            data: Dictionary with anime data.

        Returns:
            Anime object.
        """
        try:
            poster_data = data.get("image", {})
            poster = poster_data.get("original") or poster_data.get("preview")
            return Anime(
                id_=data["id"],
                title=data["titleUa"],
                poster=self._get_poster_url(poster),
                rating=data.get("malScored", 0.0),
                scored_by=data.get("malScoredBy", 0),
                type_=data.get("type", ""),
                episodes=data.get("episodes", 0),
                episodes_aired=data.get("episodesAired", 0),
                status=data.get("status", ""),
                release_year=int(data.get("releaseDate", 0)),
                producer=data.get("producer", ""),
                description=data.get("description", ""),
                mal_id=int(data.get("malId", 0)),
            )
        except (KeyError, ValueError) as error:
            logger.warning(f"Failed to parse anime data: {error}")
            return None

    def _parse_fandub(self, data: Dict[str, Any]) -> Optional[Fandub]:
        """
        Parses Fandub data from the API response.

        Args:
            data: Dictionary with fandub data.

        Returns:
            Fandub object.
        """
        try:
            fandub_data = data["fundub"]
            return Fandub(
                id_=fandub_data["id"],
                name=fandub_data["name"],
                players=[
                    Player(id_=player_data["id"], name=player_data["name"])
                    for player_data in data.get("player", [])
                ],
            )
        except (KeyError, ValueError) as error:
            logger.warning(f"Failed to parse fandub data: {error}")
            return None

    def search(self, query: str) -> Optional[List[Anime]]:
        """
        Searches for anime by query.

        Args:
            query: Search query.

        Returns:
            List of Anime objects if successful, None otherwise.
        """
        logger.info(f"Searching anime with query: {query}")

        encoded_query = normalize_query(query)
        if not encoded_query:
            logger.error("Search query is empty or contains invalid characters")
            return None

        endpoint = f"api/anime/search/{encoded_query}"
        params = {"full": "true"}
        data = self._get_data(endpoint, params)

        if not data or "result" not in data:
            logger.error("API returned invalid data")
            return None

        return [anime for item in data["result"] if (anime := self._parse_anime(item))]

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
            logger.error("API returned invalid data")
            return None

        return [Episode(id_=item["id"], episode=item["episode"]) for item in data]

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
            logger.error("API returned invalid data")
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
            logger.error("API returned invalid data")
            return None

        return [fandub for item in data if (fandub := self._parse_fandub(item))]
