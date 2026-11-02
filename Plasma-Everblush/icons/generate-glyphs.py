#!/usr/bin/env python3
"""Generate Everblush-glyphs, an icon theme that colours Tela's monochrome glyphs.

Covers the system tray and Dolphin (sidebar places, tabs and toolbar).

Run:  python3 generate-glyphs.py [--source DIR] [--out DIR]
      (defaults: source ~/.local/share/icons/Tela, out ./Everblush-glyphs)

The theme is a thin overlay on Tela (Inherits=Tela). Every icon whose name
matches a RULES pattern is copied from Tela at every size, with its
foreground (ColorScheme-Text, or a hard-coded grey in GTK-style symbolic
icons) swapped for the rule's colour. Highlight parts are swapped too, since
Tela uses them for some warning states. Full-colour icons (the big folders in
Dolphin's view, app icons) are copied unchanged. Copying every size keeps icon lookup
identical to Tela's. Icons that match no rule are left to Tela.

Colours are ColorScheme-* classes where KIconLoader has one, so they follow
the Plasma colour scheme. KIconLoader has no blue or magenta class, so those
are hard-coded from the Everblush palette (cyan too).
"""
import argparse
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "Everblush-glyphs"

# Fallback colours written into each stylesheet; Plasma replaces the class ones at runtime.
SCHEME = {
    "Text": "#dadada", "Highlight": "#6695a3", "PositiveText": "#8ccf7e",
    "NeutralText": "#e5c76b", "NegativeText": "#e06e6e",
}
BLUE = "#67b0e8"
MAGENTA = "#c47fd5"
CYAN = "#67cbe7"
GREEN, YELLOW, RED, ACCENT = "PositiveText", "NeutralText", "NegativeText", "Highlight"

# (pattern, colour). Matched against the icon name from its start; first match wins.
# A colour of None keeps the icon monochrome (it is still copied so a later rule can't catch it).
RULES = [
    # Battery and power: by charge level.
    (r"(keyboard-)?battery-(caution|empty|missing|0[01]0|level-(0|10)-)", RED),
    (r"(keyboard-)?battery-(low|0[23]0|level-[23]0-)", YELLOW),
    (r"(keyboard-)?battery|ac-adapter|speedometer|power-profile", GREEN),
    # Volume and microphone.
    (r"(audio|microphone|mic)-.*(muted|-off|-none|zero)", RED),
    (r"audio-(volume|input|output)|microphone-|mic-", ACCENT),
    # Bluetooth, before the network rules so network-bluetooth lands here.
    (r"(network-)?bluetooth.*(disabled|offline|inactive)", None),
    (r"(network-)?bluetooth|preferences-system-bluetooth", BLUE),
    # Network.
    (r"(network|nm)-.*(offline|disconnected|no-route|no-connection|unavailable|error|-off\b)", RED),
    (r"(network|nm)-.*(limited|acquiring)", YELLOW),
    (r"network-(wired|wireless|mobile|cellular|vpn)|nm-", BLUE),
    # Notifications and updates.
    (r"notifications?-disabled|notification-disabled", RED),
    (r"notification|preferences-desktop-notification", YELLOW),
    (r"update-high", RED),
    (r"update-medium|updates-notifier|system-software-update", YELLOW),
    (r"update-(low|none)", GREEN),
    # Dolphin sidebar and tabs.
    (r"user-home|go-home", ACCENT),
    (r"user-desktop", CYAN),
    (r"folder-documents", BLUE),
    (r"folder-downloads?", GREEN),
    (r"folder-music", MAGENTA),
    (r"folder-pictures", YELLOW),
    (r"folder-videos", RED),
    (r"folder-network|network-workgroup|folder-remote", CYAN),
    (r"user-trash", RED),
    (r"document-open-recent|folder-open-recent|folder-recent|view-calendar-day|go-jump-today", YELLOW),
    # Dolphin toolbar.
    (r"go-(previous|next|up|down)(-symbolic)?$|view-(list|split|preview|refresh)|edit-find"
     r"|application-menu|open-menu|view-more", ACCENT),
    # Everything else in the tray.
    (r"klipper", MAGENTA),
    (r"device-notifier|drive-removable-media", GREEN),
    (r"kdeconnect", ACCENT),
    (r"plasmavault", MAGENTA),
    (r"camera-on", RED),
    (r"redshift-status-on|night-light", YELLOW),
]
RULES = [(re.compile(p), c) for p, c in RULES]

# Greys that GTK-style symbolic icons hard-code instead of using a class.
GREY_RE = re.compile(r"#(565656|dfdfdf|bebebe|dadada)\b", re.I)
STYLE_RE = re.compile(r'<style id="current-color-scheme"[^>]*>.*?</style>', re.S)
TAG_RE = re.compile(r"<(path|g|rect|circle|ellipse|polygon|use)\b[^>]*>")
# Hard-coded colours go in their own stylesheet: KIconLoader rewrites current-color-scheme.
FIXED = {BLUE: "EverblushBlue", MAGENTA: "EverblushMagenta", CYAN: "EverblushCyan"}


def colour_for(name):
    for pat, colour in RULES:
        if pat.match(name):
            return colour, True
    return None, False


def stylesheet():
    css = " ".join(".ColorScheme-%s { color:%s; }" % kv for kv in SCHEME.items())
    return '<style id="current-color-scheme" type="text/css">%s</style>' % css


def recolour(svg, colour):
    """Point the icon's foreground at `colour` (a ColorScheme class name or '#hex')."""
    if "ColorScheme-Background" in svg:  # full-colour icon, e.g. Tela's big folders
        return svg
    cls = FIXED[colour] if colour.startswith("#") else "ColorScheme-" + colour

    def tag(m):
        t = m.group(0)
        # Tela paints some warning states with Highlight, which Plasma turns into the accent.
        if re.search(r'class="ColorScheme-(Text|Highlight)"', t):
            return re.sub(r'class="ColorScheme-(Text|Highlight)"', 'class="%s"' % cls, t)
        if "class=" not in t and GREY_RE.search(t):
            t = GREY_RE.sub("currentColor", t)
            return t.replace("<" + m.group(1), '<%s class="%s"' % (m.group(1), cls), 1)
        return t

    new = TAG_RE.sub(tag, svg)
    if new == svg:  # full-colour icon, nothing to recolour
        return svg
    svg = new
    sheet = stylesheet()
    if colour.startswith("#"):
        sheet += '<style type="text/css">.%s { color:%s; }</style>' % (cls, colour)
    if STYLE_RE.search(svg):
        return STYLE_RE.sub(lambda _: sheet, svg, count=1)
    return re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + sheet, svg, count=1)


def write_index(source, out):
    with open(os.path.join(source, "index.theme")) as fh:
        text = fh.read()
    text = re.sub(r"^Name=.*$", "Name=" + NAME, text, count=1, flags=re.M)
    text = re.sub(r"^Comment=.*$", "Comment=Tela with Everblush-coloured tray and Dolphin glyphs",
                  text, count=1, flags=re.M)
    text = re.sub(r"^Inherits=.*$", "Inherits=%s,hicolor,breeze" % os.path.basename(source.rstrip("/")),
                  text, count=1, flags=re.M)
    with open(os.path.join(out, "index.theme"), "w") as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--source", default=os.path.expanduser("~/.local/share/icons/Tela"))
    ap.add_argument("--out", default=os.path.join(HERE, NAME))
    args = ap.parse_args()
    if not os.path.isfile(os.path.join(args.source, "index.theme")):
        raise SystemExit("no icon theme at %s" % args.source)

    os.makedirs(args.out, exist_ok=True)
    write_index(args.source, args.out)
    copied = coloured = 0
    for top in sorted(os.listdir(args.source)):
        src_top = os.path.join(args.source, top)
        if os.path.islink(src_top):  # 16@2x -> 16 and friends
            dst = os.path.join(args.out, top)
            if not os.path.lexists(dst):
                os.symlink(os.readlink(src_top), dst)
            continue
        if not os.path.isdir(src_top):
            continue
        for ctx in sorted(os.listdir(src_top)):
            src_dir = os.path.join(src_top, ctx)
            if not os.path.isdir(src_dir):
                continue
            for fname in sorted(os.listdir(src_dir)):
                if not fname.endswith(".svg"):
                    continue
                colour, matched = colour_for(fname[:-4])
                if not matched:
                    continue
                with open(os.path.join(src_dir, fname), encoding="utf-8") as fh:
                    svg = fh.read()
                if colour:
                    new = recolour(svg, colour)
                    coloured += new != svg
                    svg = new
                os.makedirs(os.path.join(args.out, top, ctx), exist_ok=True)
                with open(os.path.join(args.out, top, ctx, fname), "w", encoding="utf-8") as fh:
                    fh.write(svg)
                copied += 1
    print("%s: %d icons copied, %d recoloured -> %s" % (NAME, copied, coloured, args.out))


if __name__ == "__main__":
    main()
