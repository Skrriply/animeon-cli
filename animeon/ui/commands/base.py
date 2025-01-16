from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """Base class for commands."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        """Execute the command."""
        pass
