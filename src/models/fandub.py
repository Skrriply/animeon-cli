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

    id: int
    name: str
    players: List[Player]
