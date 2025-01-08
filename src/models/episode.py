from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Episode:
    """
    Episode model.

    Attributes:
        id_: ID of the episode.
        episode: Episode number.
    """

    id_: int
    episode: int
