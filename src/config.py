import logging

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_COLORS = {
    logging.DEBUG: "\033[0;36m",  # Cyan
    logging.INFO: "\033[0;32m",  # Green
    logging.WARNING: "\033[0;33m",  # Yellow
    logging.ERROR: "\033[0;31m",  # Red
    logging.CRITICAL: "\033[0;35m",  # Magenta
}
LOG_RESET = "\033[0m"

# API configuration
API_BASE_URL = "https://animeon.club"
API_HEADERS = {"Referer": API_BASE_URL}

# Default commands
FZF_DEFAULT_COMMAND = [
    "fzf",
    "--reverse",
    "--cycle",
    "--border=rounded",
    "--preview-window=left:30%:wrap,border-rounded",
    "--pointer=❯",
    "--marker=◆ ",
]
MPV_DEFAULT_COMMAND = ["mpv"]

# Required system dependencies
DEPENDENCIES = {"fzf": ["fzf", "--version"], "mpv": ["mpv", "--version"]}
