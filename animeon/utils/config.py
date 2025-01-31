import logging
from pathlib import Path
from typing import Any, Optional

import toml

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration."""

    def __init__(self, config_path: Path, default_config: str) -> None:
        """
        Initializes the class.

        Args:
            config_path: The path to the configuration file.
            default_config: The default configuration as a string.
        """
        self.config = {}
        self.config_path = config_path
        self.default_config = default_config

        if self.config_path.exists():
            self._load()
        else:
            self._create()
            self._load()

    def _create(self) -> None:
        """Creates a new configuration file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as file:
            file.write(self.default_config)

        logger.debug(f"Configuration created at: {self.config_path}")

    def _load(self) -> None:
        """Loads configuration from the TOML file."""
        logger.debug(f"Loading configuration from: {self.config_path}")

        try:
            self.config = toml.load(self.config_path)
        except toml.TomlDecodeError as error:
            logger.error(f"Error decoding TOML file: {error}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value using a dot-notation key.

        Args:
            key: The key to retrieve (e.g., "api.timeout").
            default: The default value to return if the key isn't found.

        Returns:
            The configuration value or the default if not found.
        """
        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Key '{key}' not found, returning default: {default}")
            return default
