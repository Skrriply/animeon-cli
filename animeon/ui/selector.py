import logging
from typing import List, Optional

from animeon.models import Anime, Episode, Fandub, Player

from .preview import AnimePreviewGenerator
from .prompt import Prompt

logger = logging.getLogger(__name__)


class ContentSelector:
    """Class for selecting anime content."""

    def __init__(
        self, prompt: Prompt, preview_generator: AnimePreviewGenerator
    ) -> None:
        """
        Initializes the class.

        Args:
            prompt: Interface for user prompting.
            preview_generator: Object for creating previews of anime content.
        """
        self.prompt = prompt
        self.preview_generator = preview_generator

    def select_anime(self, anime_list: List[Anime]) -> Optional[Anime]:
        """
        Selects anime from the list.

        Args:
            anime_list: List of anime.

        Returns:
            Selected anime or None if no anime is selected.
        """
        preview_file = self.preview_generator.generate(anime_list)
        anime_titles = [anime.title for anime in anime_list]
        selected_title = self.prompt.single_select(
            "Оберіть аніме: ", anime_titles, preview_file=preview_file
        )

        if not selected_title:
            logger.info("Anime not selected")
            return None

        return next(anime for anime in anime_list if anime.title == selected_title)

    def select_fandub(self, fandubs: List[Fandub]) -> Optional[Fandub]:
        """
        Selects fandub from the list.

        Args:
            fandubs: List of fandubs.

        Returns:
            Selected fandub or None if no fandub is selected.
        """
        fandub_names = [fandub.name for fandub in fandubs]
        selected_name = self.prompt.single_select("Оберіть озвучення: ", fandub_names)

        if not selected_name:
            logger.info("Fandub not selected")
            return None

        return next(fandub for fandub in fandubs if fandub.name == selected_name)

    def select_player(self, players: List[Player]) -> Optional[Player]:
        """
        Selects player from the list.

        Args:
            players: List of players.

        Returns:
            Selected player or None if no player is selected.
        """
        player_names = [player.name for player in players]
        selected_name = self.prompt.single_select("Оберіть плеєр: ", player_names)

        if not selected_name:
            logger.info("Player not selected")
            return None

        return next(player for player in players if player.name == selected_name)

    def select_episodes(self, episodes: List[Episode]) -> Optional[List[Episode]]:
        """
        Selects episodes from the list.

        Args:
            episodes: List of episodes.

        Returns:
            Selected episodes or None if no episode is selected.
        """
        episode_options = [f"Епізод {episode.episode}" for episode in episodes]
        selected_options = self.prompt.multi_select(
            "Оберіть епізоди: ", episode_options
        )

        if not selected_options:
            logger.info("Episodes not selected")
            return None

        return [
            episode
            for episode in episodes
            if f"Епізод {episode.episode}" in selected_options
        ]
