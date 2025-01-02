import logging

from src.core.api import AnimeAPI
from src.ui.player import VideoPlayer
from src.ui.selector import ContentSelector

from .base import BaseCommand

logger = logging.getLogger(__name__)


class SearchCommand(BaseCommand):
    """Command for searching and playing anime."""

    name = "search"
    desciption = "Пошук та перегляд аніме."

    def __init__(
        self,
        api_client: AnimeAPI,
        selector: ContentSelector,
        player: VideoPlayer,
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
        logger.info(f"Пошук аніме за запитом: {query}")

        # Gets search results
        search_results = self.api.search(query)
        if not search_results:
            logging.error("Аніме не знайдено.")
            return

        logger.debug(f"Знайдено {len(search_results)} результатів пошуку.")

        # Selects anime
        selected_anime = self.selector.select_anime(search_results)
        if not selected_anime:
            logging.info("Аніме не обрано.")
            return

        logger.debug(f"Обрано аніме: {selected_anime.title}")

        # Gets fandub
        fandubs = self.api.get_fandubs_and_players(selected_anime.id_)
        if not fandubs:
            logging.error("Озвучень для цього аніме не знайдено.")
            return

        logger.debug(f"Знайдено {len(fandubs)} озвучень для цього аніме.")

        # Selects fandub
        selected_fandub = self.selector.select_fandub(fandubs)
        if not selected_fandub:
            logging.info("Озвучення не обрано.")
            return

        logger.debug(f"Обрано озвучення: {selected_fandub.name}")

        # Gets player
        players = selected_fandub.players
        if not players:
            logging.error("Плеєрів для цього озвучення не знайдено.")

        logger.debug(f"Знайдено {len(players)} плеєрів для цього озвучення.")

        # Selects player
        selected_player = self.selector.select_player(players)
        if not selected_player:
            logging.info("Плеєр не обрано.")
            return

        logger.debug(f"Обрано плеєр: {selected_player.name}")

        # Gets episodes
        episodes = self.api.get_episodes(selected_player.id_, selected_fandub.id_)
        if not episodes:
            logging.error("Епізодів не знайдено.")
            return

        logger.debug(f"Знайдено {len(episodes)} епізодів.")

        # Selects episodes
        selected_episodes = self.selector.select_episodes(episodes)
        if not selected_episodes:
            logging.info("Епізоди не обрано.")
            return

        logger.debug(f"Обрано {len(selected_episodes)} епізодів.")

        # Gets video URLs for selected episodes
        episode_ids = [episode.id_ for episode in selected_episodes]
        urls = [self.api.get_video_url(id) for id in episode_ids]
        if not urls:
            logging.error("Посилань на епізоди не знайдено.")
            return

        logger.debug(f"Знайдено {len(urls)} посилань на епізоди.")

        if None in urls:
            logger.warning("Деякі посилання на епізоди відсутні.")
            urls = [url for url in urls if url is not None]

        self.player.play(urls)  # type: ignore
