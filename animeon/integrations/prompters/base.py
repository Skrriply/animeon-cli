from abc import ABC, abstractmethod
from typing import List, Optional


class BasePrompter(ABC):
    """Abstract base class for prompters."""

    @abstractmethod
    def prompt(self, options: List[str], title: Optional[str] = None) -> Optional[str]:
        """
        Prompts the user to select an option from a list of options.

        Args:
            options: A list of options to select from.
            title: Optional title to display.

        Returns:
            The selected option, or None if no option was selected or if an error occurred.
        """
        pass
