BASE_URL = "https://animeon.club"
HEADERS = {"Referer": BASE_URL}

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
