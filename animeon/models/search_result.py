from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SearchResult:
    """
    Search result model.

    Attributes:
        id_: ID of the anime.
        title: Title of the anime.
    """

    id_: int
    title: str
