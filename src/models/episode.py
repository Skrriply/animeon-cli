from dataclasses import dataclass


@dataclass
class Episode:
    """
    Episode model.

    Attributes:
        id: ID of the episode.
        episode: Episode number.
    """

    id: int
    episode: int
