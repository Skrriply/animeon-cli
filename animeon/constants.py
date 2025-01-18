import logging
from pathlib import Path

import colorama

CONFIG_PATH = Path.home() / ".config" / "animeon" / "config.toml"
DEFAULT_CONFIG = {
    "api": {"timeout": 30},
    "logging": {
        "level": "ERROR",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "date_format": "%Y-%m-%d %H:%M:%S",
    },
}

COLORS = {
    logging.DEBUG: colorama.Fore.CYAN,
    logging.INFO: colorama.Fore.GREEN,
    logging.WARNING: colorama.Fore.YELLOW,
    logging.ERROR: colorama.Fore.RED,
    logging.CRITICAL: colorama.Fore.MAGENTA,
}
RESET = colorama.Style.RESET_ALL

API_BASE_URL = "https://animeon.club"

FZF_BASE_COMMAND = [
    "fzf",
    "--reverse",
    "--cycle",
    "--border=rounded",
    "--preview-window=left:30%:wrap,border-rounded",
    "--pointer=❯",
    "--marker=◆ ",
]
MPV_COMMAND = ["mpv"]
CHAFA_BASE_COMMAND = ["chafa", "--size=45x25"]

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
