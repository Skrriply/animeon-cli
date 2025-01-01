import re
from dataclasses import dataclass
from typing import List


@dataclass
class Anime:
    """
    Anime model.

    Attributes:
        id_: ID of the anime.
        title: Title of the anime.
        poster: URL of the anime poster.
        rating: MyAnimeList rating of the anime.
        scored_by: Number of users who scored the anime.
        type_: Type of the anime. (TV, OVA, ONA, Movie or Special)
        episodes: Number of episodes of the anime.
        episodes_aired: Number of episodes aired of the anime.
        status: Status of the anime.
        genres: List of genres of the anime.
        release_year: Year the anime was released.
        studio: Studio that produced the anime.
        producer: Producer of the anime.
        description: Description of the anime.
        mal_id: MyAnimeList ID of the anime.
    """

    id_: int
    title: str
    poster: str
    rating: float
    scored_by: int
    type_: str
    episodes: int
    episodes_aired: int
    status: str
    genres: List[str]
    release_year: int
    studio: str
    producer: str
    description: str
    mal_id: int

    def __post_init__(self) -> None:
        """
        Post initialization method.
        """
        if self.description:
            self.description = self._clean_description(self.description)

    @staticmethod
    def _clean_description(text: str) -> str:
        """
        Cleans description from Markdown links.

        Args:
            text: Description to clean.

        Returns:
            Cleaned description.
        """
        # Removes Markdown links
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        text = re.sub(r"<(http[s]?://\S+)>", r"\1", text)

        return text.strip()
