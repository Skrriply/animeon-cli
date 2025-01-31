#!/usr/bin/env bash
# ──────────────────────────────────────────
# Script for previewing anime content in fzf
# ──────────────────────────────────────────
# Original script:
# https://github.com/junegunn/fzf/blob/master/bin/fzf-preview.sh
# ──────────────────────────────────────────
# Dependencies:
# - https://github.com/jqlang/jq
# - https://github.com/kovidgoyal/kitty (optional)
# - https://github.com/hpjansson/chafa (optional)
# ──────────────────────────────────────────

# Gets data from given JSON file
poster=$(jq --raw-output ".[\"$1\"].poster_path" "$2")
preview_text=$(jq --raw-output ".[\"$1\"].text_content" "$2")

# Uses smaller size for preview
width=$FZF_PREVIEW_COLUMNS
height=$((FZF_PREVIEW_LINES - 10))

# Generates separator based on FZF_PREVIEW_COLUMNS
separator=""
for ((i=0; i < ${FZF_PREVIEW_COLUMNS:-1}; i++)); do
  separator+="─"
done

# Replaces "{separator}" with the generated separator
preview_text="${preview_text//\{separator\}/$separator}"


# Displays image with kitty icat
display_image_kitty() {
    # 1. 'memory' is the fastest option but if you want the image to be scrollable,
    #    you have to use 'stream'.
    #
    # 2. The last line of the output is the ANSI reset code without newline.
    #    This confuses fzf and makes it render scroll offset indicator.
    #    So we remove the last line and append the reset code to its previous line.
    kitty icat --clear --transfer-mode=stream --unicode-placeholder --stdin=no --scale-up --place="${width}x${height}@0x0" "$poster" | sed '$d' | sed $'$s/$/\e[m/'
}

# Displays image with chafa
display_image_chafa() {
    chafa --clear --size="${width}x${height}" "$poster"

    # Adds a new line character so that fzf can display multiple images in the preview window
    echo
}

# Displays image
if [[ -n "$poster" ]]; then
    # 1. Kitty icat on kitty terminal
    if [[ $KITTY_WINDOW_ID ]]; then
        display_image_kitty

    # 2. Chafa
    elif command -v chafa >/dev/null; then
        display_image_chafa
    fi
fi

echo -e "$preview_text"
