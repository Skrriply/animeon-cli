from dataclasses import dataclass
from typing import Type, TypeVar

T = TypeVar("T", bound="BaseConfig")


@dataclass
class BaseConfig:
    """Base configuration class."""

    @classmethod
    def default(cls: Type[T]) -> T:
        """
        Creates default configuration instance.

        Args:
            cls: Class type.

        Returns:
            Default configuration instance.
        """
        raise NotImplementedError
