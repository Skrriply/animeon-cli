from dataclasses import dataclass


@dataclass
class Anime:
    """
    Anime model.

    Attributes:
        id: ID of the anime.
        mal_id: MyAnimeList ID.
        title: Title of the anime.
    """

    id: int
    mal_id: int
    title: str
