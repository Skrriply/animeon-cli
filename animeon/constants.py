from pathlib import Path

# Path to user's home directory
HOME_DIR = Path.home()

# Path to the application configuration file
CONFIG_PATH = HOME_DIR / ".config" / "animeon" / "config.toml"

# Path to the application cache directory
CACHE_DIR = HOME_DIR / ".cache" / "animeon"

# Default configuration settings
DEFAULT_CONFIG = """# ─────────────────────────────────────────────────────────────────
# ▄▀▄ █▄ █ █ █▄ ▄█ ██▀ ▄▀▄ █▄ █   ▄▀▀ █   █   ▄▀▀ ▄▀▄ █▄ █ █▀ █ ▄▀
# █▀█ █ ▀█ █ █ ▀ █ █▄▄ ▀▄▀ █ ▀█   ▀▄▄ █▄▄ █   ▀▄▄ ▀▄▀ █ ▀█ █▀ █ ▀▄█
# ─────────────────────────────────────────────────────────────────
[logging]
# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
level = "ERROR"

# Format for log messages
# See https://docs.python.org/3/library/logging.html#logrecord-attributes
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Date format for log messages
# See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
date_format = "%Y-%m-%d %H:%M:%S"

[api]
# Timeout for API requests in seconds
timeout = 10

[ui]
# Default UI to use (now only fzf is supported)
default = "fzf"

[ui.fzf]
# Enable preview mode
preview = true

# Extra arguments to pass to fzf
# It is not recommended to use --prompt and --preview,
# as they are automatically added by the application
extra_args = ["--reverse", "--cycle", "--border=rounded", "--preview-window=left,30%,wrap", "--pointer=❯", "--marker=◆ "]

[player]
# Default player to use (now only mpv is supported)
default = "mpv"

[player.mpv]
# Extra arguments to pass to mpv
# It is not recommended to use --title,
# as it is automatically added by the application
extra_args = []
"""

# Mapping of anime types and statuses to their names
ANIME_TYPES = {
    "tv": "ТБ-серіал",
    "movie": "Фільм",
    "ova": "OVA",
    "ona": "ONA",
    "special": "Спешл",
}
ANIME_STATUSES = {
    "ongoing": "Онґоінґ",
    "released": "Завершено",
    "anons": "Незабаром",
}
