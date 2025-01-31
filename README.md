<div align="center">

# ⛩️ AnimeOn CLI

Простий CLI інструмент для пошуку та відтворення аніме з [AnimeOn](https://animeon.club/)

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://github.com/Skrriply/animeon-cli/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/Skrriply/animeon-cli)](https://github.com/Skrriply/animeon-cli/issues)

_🌟 Натхнений [ani-cli](https://github.com/pystardust/ani-cli)_

</div>

## 🔐 Залежності

| Назва                                                                                                | Опис                                                                                                                                                                                                                   | Обов'язково |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| [Python](https://www.python.org)                                                                     | Інтерпретатор Python. Необхідний для запуску застосунку. Переконайтеся, що встановлено Python версії 3.10 або новіше та він доступний в PATH вашої операційної системи.                                                                 | ✅          |
| [mpv](https://github.com/mpv-player/mpv)                                                             | Потужний відеоплеєр для відтворення епізодів аніме.                                                                                                                                                                    | ✅          |
| [fzf](https://github.com/junegunn/fzf)                                                               | Універсальний CLI застосунок для нечіткого пошуку. Забезпечує гарний користувацький інтерфейс.                                                                                                                         | ✅          |
| [bash](https://www.gnu.org/software/bash)                                                            | Оболонка Bash. Використовується для виконання скрипта `fzf_preview.sh`, що відповідає за створення прев'ю. Необхідний для роботи функції попереднього перегляду в `fzf`.                                               | ✅          |
| [jq](https://github.com/jqlang/jq)                                                                   | JSON процесор. Використовується у `fzf_preview.sh` для обробки JSON даних попереднього перегляду аніме.                                                                                                                | ✅          |
| [chafa](https://github.com/hpjansson/chafa)                                                          | Застосунок командного рядка для відображення аніме постерів у `fzf`. Якщо не встановлено, попередній перегляд постерів не відображатиметься.                                                                           | ❌          |
| [kitty](https://github.com/kovidgoyal/kitty) та [icat](https://sw.kovidgoyal.net/kitty/kittens/icat) | Швидкий та багатофункціональний емулятор терміналу й інструмент командного рядка для відображення зображень у цьому терміналі. Забезпечує відображення аніме постерів у  `fzf`, якщо ви використовуєте термінал kitty. | ❌          |

## 🚀 Встановлення

<details>
<summary><b>Linux</b></summary>

### 1. Встановлення системних залежностей та pipx

Встановіть [необхідні залежності](#-залежності) та [pipx](https://github.com/pypa/pipx) через ваш улюблений пакетний менеджер

### 2. Встановлення застосунку

#### Через pipx та Git (рекомендовано)

```bash
pipx install git+https://github.com/Skrriply/animeon-cli.git
```

#### Через pipx (без Git)

```bash
pipx install https://github.com/Skrriply/animeon-cli/archive/refs/heads/main.zip
```

</details>

## 🔁 Оновлення

<details>
<summary><b>Linux</b></summary>

```bash
pipx upgrade animeon
```

</details>

## 🗑️ Видалення

<details>
<summary><b>Linux</b></summary>

```bash
pipx uninstall animeon
```

</details>

## ⚖️ Ліцензія

Цей проєкт поширюється за ліцензією [GPL-3.0](https://github.com/Skrriply/animeon-cli/blob/main/LICENSE).
