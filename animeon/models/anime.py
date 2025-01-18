import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass(slots=True)
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
        studio: Studio that produced the anime.
        release_year: Year the anime was released.
        epidode_duration: Duration of each episode.
        producer: Producer of the anime.
        description: Description of the anime.
        mal_id: MyAnimeList ID of the anime.
    """

    id_: int
    title: str
    poster: Optional[str]
    rating: Optional[float]
    scored_by: Optional[int]
    type_: Optional[str]
    episodes: Optional[int]
    episodes_aired: Optional[int]
    status: Optional[str]
    genres: Optional[List[str]]
    studio: Optional[str]
    release_year: Optional[int]
    episode_duration: Optional[str]
    producer: Optional[str]
    description: Optional[str]
    mal_id: Optional[int]

    def __post_init__(self) -> None:
        """
        Post initialization method.
        """
        self.title = self.title.strip()
        if self.description:
            self.description = self._clean_text(self.description)

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Cleans text from Markdown links.

        Args:
            text: Text to clean.

        Returns:
            Cleaned text.
        """
        # Removes Markdown links
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        text = re.sub(r"<(http[s]?://\S+)>", r"\1", text)

        return text.strip()
