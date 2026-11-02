#!/usr/bin/env bash
# Install the Everblush theme set for KDE Plasma 6 into the current user's home.
# Usage: ./install.sh            copy files only
#        ./install.sh --apply    copy files and apply everything to the running session
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

copy() {  # copy <src-dir> <dest-parent>
  local src="$1" dest="$2"
  [[ -e "$src" ]] || { echo "skip: $src not found"; return; }
  mkdir -p "$dest"
  rm -rf "$dest/$(basename "$src")"
  cp -a "$src" "$dest/"
  echo "installed: $dest/$(basename "$src")"
}

copy "$SRC/color-schemes/Everblush.colors"          "$DATA/color-schemes"
copy "$SRC/konsole/Everblush.colorscheme"           "$DATA/konsole"
copy "$SRC/plasma/desktoptheme/Everblush"           "$DATA/plasma/desktoptheme"
copy "$SRC/aurorae/themes/Everblush"                "$DATA/aurorae/themes"

# Everblush-glyphs is generated from the installed Tela icons rather than shipped.
TELA="$DATA/icons/Tela"
if [[ -f "$TELA/index.theme" ]]; then
  rm -rf "$DATA/icons/Everblush-glyphs"
  python3 "$SRC/icons/generate-glyphs.py" --source "$TELA" --out "$DATA/icons/Everblush-glyphs"
else
  echo "skip: Everblush-glyphs needs the Tela icon theme in $TELA"
fi

if (( APPLY )); then
  plasma-apply-colorscheme Everblush
  plasma-apply-desktoptheme Everblush
  /usr/libexec/kwin-applywindowdecoration __aurorae__svg__Everblush
  [[ -d "$DATA/icons/Everblush-glyphs" ]] && /usr/libexec/plasma-changeicons Everblush-glyphs
  # Match xfwm: title on the left, buttons minimize/maximize/close on the right.
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft  ""
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight "IAX"
  dbus-send --session --type=signal /KWin org.kde.KWin.reloadConfig
  echo "Applied. Set Konsole's profile color scheme to 'Everblush' in Konsole > Settings."
else
  echo
  echo "Files installed. Apply them in System Settings > Colors & Themes, or run: $0 --apply"
fi
