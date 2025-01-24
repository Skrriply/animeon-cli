import logging
from typing import Any, Optional

import toml

from animeon.constants import CONFIG_PATH, DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration."""

    def __init__(self) -> None:
        """Initializes the class."""
        self._config = {}
        self._load_config()

    def _load_config(self) -> None:
        """Loads configuration from the TOML file."""
        if CONFIG_PATH.exists():
            logger.debug(f"Loading configuration from: {CONFIG_PATH}")
            try:
                self._config = toml.load(CONFIG_PATH)
            except toml.TomlDecodeError as e:
                logger.error(f"Error decoding TOML file: {e}")
                self._config = {}
        else:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            logger.debug("Configuration file not found, using default settings.")
            self._config = DEFAULT_CONFIG
            self.save()

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
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Key '{key}' not found, returning default: {default}")
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Sets a configuration value using a dot-notation key.
        Creates nested dictionaries if necessary.

        Args:
             key: The key to set (e.g., "api.timeout").
             value: The value to set.
        """
        keys = key.split(".")
        current = self._config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        logger.debug(f"Set config value: {key} = {value}")

    def save(self) -> None:
        """Saves the current configuration to the TOML file."""
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                toml.dump(self._config, file)
            logger.debug(f"Configuration saved to: {CONFIG_PATH}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
