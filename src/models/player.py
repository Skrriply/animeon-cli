from dataclasses import dataclass


@dataclass
class Player:
    """
    Player model.

    Attributes:
        id_: ID of the player.
        name: Name of the player.
    """

    id_: int
    name: str
