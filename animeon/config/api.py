from dataclasses import dataclass
from typing import Type

from .base import BaseConfig


@dataclass
class ApiConfig(BaseConfig):
    timeout: int

    @classmethod
    def default(cls: Type["ApiConfig"]) -> "ApiConfig":
        """
        Creates default configuration.

        Args:
            cls: Class type.

        Returns:
            Default ApiConfig instance.
        """
        return cls(timeout=30)
