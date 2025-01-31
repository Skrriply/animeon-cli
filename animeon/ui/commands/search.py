import logging

from animeon.core.api import AnimeOnAPI
from animeon.integrations.players import BasePlayer
from animeon.ui.selector import ContentSelector

from .base import BaseCommand

logger = logging.getLogger(__name__)


class SearchCommand(BaseCommand):
    """Command for searching and playing anime."""

    def __init__(
        self,
        api_client: AnimeOnAPI,
        selector: ContentSelector,
        player: BasePlayer,
    ) -> None:
        """
        Initializes the command.

        Args:
            api_client: AnimeON API client.
            selector: Selector for anime content.
            player: Video player.
        """
        self.api = api_client
        self.selector = selector
        self.player = player

    def execute(self, query: str) -> None:
        logger.info(f"Searching anime for query: {query}")

        # Gets search results
        search_results = self.api.search(query)
        if not search_results:
            logging.error("Search results not found")
            return

        logger.debug(f"Found {len(search_results)} search results")

        # Gets anime
        anime_list = [
            anime
            for result in search_results
            if (anime := self.api.get_anime(result.id_))
        ]
        if not anime_list:
            logging.error("Anime not found")
            return

        logger.debug(f"Found {len(anime_list)} anime")

        # Selects anime
        selected_anime = self.selector.select_anime(anime_list)
        if not selected_anime:
            logging.info("Anime not selected")
            return

        logger.debug(f"Selected anime: {selected_anime.title}")

        # Gets fandub
        fandubs = self.api.get_fandubs_and_players(selected_anime.id_)
        if not fandubs:
            logging.error("No fandubs found for this anime")
            return

        logger.debug(f"Found {len(fandubs)} fandubs for this anime")

        # Selects fandub
        selected_fandub = self.selector.select_fandub(fandubs)
        if not selected_fandub:
            logging.info("Fandub not selected")
            return

        logger.debug(f"Selected fandub: {selected_fandub.name}")

        # Gets player
        players = selected_fandub.players
        if not players:
            logging.error("No players found for this fandub")

        logger.debug(f"Found {len(players)} players for this fandub")

        # Selects player
        selected_player = self.selector.select_player(players)
        if not selected_player:
            logging.info("Player not selected")
            return

        logger.debug(f"Selected player: {selected_player.name}")

        # Gets episodes
        episodes = self.api.get_episodes(selected_player.id_, selected_fandub.id_)
        if not episodes:
            logging.error("No episodes found")
            return

        logger.debug(f"Found {len(episodes)} episodes")

        while True:
            # Selects episodes
            selected_episode = self.selector.select_episode(episodes)
            if not selected_episode:
                logging.info("Episode not selected")
                return

            logger.debug(f"Selected {selected_episode.episode} episode")

            # Gets video URLs for selected episodes
            url = self.api.get_video_url(selected_episode.id_)
            if not url:
                logging.error("No episode link found")
                return

            # TODO: Add check for MpvPlayer
            self.player.play(
                url,
                title=f"{selected_anime.title} - Епізод {selected_episode.episode}",  # type: ignore
            )
