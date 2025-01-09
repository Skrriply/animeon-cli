from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Base class for commands."""

    name: str = ""
    desciption: str = ""

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        """Execute the command."""
        pass
