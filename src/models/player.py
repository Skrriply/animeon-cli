from dataclasses import dataclass


@dataclass
class Player:
    """
    Player model.

    Attributes:
        id: ID of the player.
        name: Name of the player.
    """

    id: int
    name: str
