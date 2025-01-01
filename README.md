<div align="center">

# ⛩️ AnimeOn CLI

Простий CLI інструмент для пошуку та відтворення аніме з сайту [AnimeOn](https://animeon.club/)

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://github.com/Skrriply/animeon-cli/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/Skrriply/animeon-cli)](https://github.com/Skrriply/animeon-cli/issues)

_Натхнений [ani-cli](https://github.com/pystardust/ani-cli)_

</div>

## 🔐 Залежності

### Необхідні компоненти

- [Python 3.10+](https://www.python.org/downloads/) - інтерпретатор Python
- [mpv](https://github.com/mpv-player/mpv) - відеоплеєр
- [fzf](https://github.com/junegunn/fzf) - інтерактивний пошук
- [chafa](https://github.com/hpjansson/chafa) - відображення зображень
- [jq](https://github.com/jqlang/jq) - оброблення JSON

## 🚀 Встановлення

<details>
<summary><b>Linux</b></summary>

### 1️⃣ Встановлення системних залежностей та pipx

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip pipx mpv fzf
```

#### Arch Linux

```bash
sudo pacman -S python python-pip python-pipx mpv fzf
```

#### OpenSUSE Tumbleweed

```bash
sudo zypper refresh
sudo zypper install python311 python311-pip python311-pipx mpv fzf
```

### 2️⃣ Встановлення застосунку

#### Через pipx та Git (рекомендовано)

```bash
pipx install git+https://github.com/Skrriply/animeon-cli.git
```

#### Альтернативний спосіб (без Git)

```bash
pipx install https://github.com/Skrriply/animeon-cli/archive/refs/heads/main.zip
```

</details>

## 🗑️ Видалення

```bash
pipx uninstall animeon
```

## ⚖️ Ліцензія

Цей проєкт поширюється за ліцензією [GPL-3.0](https://github.com/Skrriply/animeon-cli/blob/main/LICENSE).
