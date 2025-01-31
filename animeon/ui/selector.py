import logging
from pathlib import Path
from typing import List, Optional

from animeon.integrations.prompters.base import BasePrompter
from animeon.models import Anime, Episode, Fandub, Player
from animeon.utils.preview import AnimePreviewGenerator

logger = logging.getLogger(__name__)


class ContentSelector:
    """Class for selecting anime content."""

    def __init__(
        self, prompter: BasePrompter, preview_generator: AnimePreviewGenerator
    ) -> None:
        """
        Initializes the class.

        Args:
            prompter: Interface for user prompting.
            preview_generator: Object for creating previews of anime content.
        """
        self.prompter = prompter
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

        script = Path.cwd() / "animeon" / "scripts" / "fzf_preview.sh"

        # TODO: Add check for FzfPrompter
        selected_title = self.prompter.prompt(
            anime_titles,
            title="Оберіть аніме: ",
            preview_command=f"sh {script} {{}} {preview_file}",  # type: ignore
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
        selected_name = self.prompter.prompt(fandub_names, title="Оберіть озвучення: ")

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
        selected_name = self.prompter.prompt(player_names, title="Оберіть плеєр: ")

        if not selected_name:
            logger.info("Player not selected")
            return None

        return next(player for player in players if player.name == selected_name)

    def select_episode(self, episodes: List[Episode]) -> Optional[Episode]:
        """
        Selects episode from the list.

        Args:
            episodes: List of episodes.

        Returns:
            Selected episode or None if no episode is selected.
        """
        episode_options = [f"Епізод {episode.episode}" for episode in episodes]
        selected_episode = self.prompter.prompt(
            episode_options, title="Оберіть епізоди: "
        )

        if not selected_episode:
            logger.info("Episode not selected")
            return None

        return next(
            episode
            for episode in episodes
            if f"Епізод {episode.episode}" == selected_episode
        )
