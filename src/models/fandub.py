from dataclasses import dataclass
from typing import List

from .player import Player


@dataclass
class Fandub:
    """
    Fandub model.

    Attributes:
        id: ID of the fandub.
        name: Name of the fandub.
        players: List of players associated with this fandub.
    """

    id_: int
    name: str
    players: List[Player]

    def __post_init__(self) -> None:
        """
        Post initialization method.
        """
        # Some names have extra spaces
        # For example: " Glass Moon" with ID 1472
        self.name = self.name.strip()
