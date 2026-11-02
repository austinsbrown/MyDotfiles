#!/usr/bin/env python3
"""Generate the Everblush Aurorae theme (port of the xfwm4 theme Everblush-xfwm).

Writes decoration.svg and the button SVGs into themes/Everblush/.
Layout numbers must stay in sync with themes/Everblush/Everblushrc.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes", "Everblush")

# palette
TITLE = "#21282a"
HOVER = "#2c3335"
PRESS = "#363d3f"
INACT = "#dadada"

# geometry (keep in sync with Everblushrc)
TITLE_H = 36            # BorderTop = TitleHeight + TitleEdgeTop/Bottom
B = 4                   # BorderLeft/Right/Bottom (xfwm side frame was 4px)
PL, PR, PT, PB = 16, 16, 12, 20   # Padding* = shadow area
RADIUS = 4              # top corner radius (<= B so it fits in the corner slice)
SH_R, SH_DY = 16, 4     # shadow blur reach and downward offset (PT = R - DY, PB = R + DY)
assert PT == SH_R - SH_DY and PB == SH_R + SH_DY and PL == SH_R and PR == SH_R
EDGE = 10               # length of the stretchable edge / center slices

# rough gaussian falloff: (distance / SH_R, relative alpha)
FALLOFF = [(0.0, 1.0), (0.2, 0.72), (0.4, 0.42), (0.6, 0.20), (0.8, 0.07), (1.0, 0.0)]

_gid = [0]


def fmt(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def stops(a0):
    return "".join('<stop offset="%s" stop-color="#000000" stop-opacity="%s"/>' % (fmt(o), fmt(a * a0))
                   for o, a in FALLOFF)


def rect(x, y, w, h, fill, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s/>' % (fmt(x), fmt(y), fmt(w), fmt(h), fill, extra)


def bounds(x, y, w, h):
    # invisible rect that pins the element's bounding box to the exact slice size
    return rect(x, y, w, h, "#000000", ' fill-opacity="0"')


def shadow_cells(defs, sx, sy, sw, sh, R, a0):
    """Fill slice [sx,sx+sw]x[sy,sy+sh] with the shadow of rect R=(x0,y0,x1,y1)."""
    x0, y0, x1, y1 = R
    xs = sorted(set([sx, sx + sw] + [v for v in (x0, x1) if sx < v < sx + sw]))
    ys = sorted(set([sy, sy + sh] + [v for v in (y0, y1) if sy < v < sy + sh]))
    out = []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx0, cx1, cy0, cy1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            hx = "l" if cx1 <= x0 else ("r" if cx0 >= x1 else "m")
            vy = "t" if cy1 <= y0 else ("b" if cy0 >= y1 else "m")
            _gid[0] += 1
            gid = "s%d" % _gid[0]
            if hx == "m" and vy == "m":
                out.append(rect(cx0, cy0, cx1 - cx0, cy1 - cy0, "#000000", ' fill-opacity="%s"' % fmt(a0)))
                continue
            if hx != "m" and vy != "m":
                ccx = x0 if hx == "l" else x1
                ccy = y0 if vy == "t" else y1
                defs.append('<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" fx="%s" fy="%s" r="%s">%s</radialGradient>'
                            % (gid, fmt(ccx), fmt(ccy), fmt(ccx), fmt(ccy), fmt(SH_R), stops(a0)))
            else:
                if hx == "l":
                    g = (x0, 0, x0 - SH_R, 0)
                elif hx == "r":
                    g = (x1, 0, x1 + SH_R, 0)
                elif vy == "t":
                    g = (0, y0, 0, y0 - SH_R)
                else:
                    g = (0, y1, 0, y1 + SH_R)
                defs.append('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'
                            % ((gid,) + tuple(fmt(v) for v in g) + (stops(a0),)))
            out.append(rect(cx0, cy0, cx1 - cx0, cy1 - cy0, "url(#%s)" % gid))
    return out


def frame_set(defs, prefix, ox, oy, a0):
    """A normal (shadowed) frame laid out as a mini window at (ox, oy)."""
    LW, RW = PL + B, PR + B
    TH, BH = PT + TITLE_H, B + PB
    W = LW + EDGE + RW
    H = TH + EDGE + BH
    # window (decoration) rect and the offset shadow-caster rect, absolute coords
    wx0, wy0, wx1, wy1 = ox + PL, oy + PT, ox + W - PR, oy + H - PB
    R = (wx0, wy0 + SH_DY, wx1, wy1 + SH_DY)
    cols = [(ox, LW), (ox + LW, EDGE), (ox + LW + EDGE, RW)]
    rows = [(oy, TH), (oy + TH, EDGE), (oy + TH + EDGE, BH)]
    names = [["topleft", "top", "topright"], ["left", "center", "right"], ["bottomleft", "bottom", "bottomright"]]
    out = []
    r = RADIUS
    for j, (sy, sh) in enumerate(rows):
        for i, (sx, sw) in enumerate(cols):
            name = names[j][i]
            parts = [bounds(sx, sy, sw, sh)]
            if name != "center":
                parts += shadow_cells(defs, sx, sy, sw, sh, R, a0)
            # opaque window part of this slice
            if name == "topleft":
                parts.append('<path d="M%s,%s V%s A%s,%s 0 0 1 %s,%s H%s V%s Z" fill="%s"/>' % (
                    fmt(wx0), fmt(sy + sh), fmt(wy0 + r), r, r, fmt(wx0 + r), fmt(wy0), fmt(sx + sw), fmt(sy + sh), TITLE))
            elif name == "topright":
                parts.append('<path d="M%s,%s V%s A%s,%s 0 0 0 %s,%s H%s V%s Z" fill="%s"/>' % (
                    fmt(wx1), fmt(sy + sh), fmt(wy0 + r), r, r, fmt(wx1 - r), fmt(wy0), fmt(sx), fmt(sy + sh), TITLE))
            elif name == "top":
                parts.append(rect(sx, wy0, sw, sy + sh - wy0, TITLE))
            elif name == "center":
                parts.append(rect(sx, sy, sw, sh, TITLE))
            elif name == "left":
                parts.append(rect(wx0, sy, B, sh, TITLE))
            elif name == "right":
                parts.append(rect(wx1 - B, sy, B, sh, TITLE))
            elif name == "bottom":
                parts.append(rect(sx, sy, sw, B, TITLE))
            elif name == "bottomleft":
                parts.append(rect(wx0, sy, B, B, TITLE))
            elif name == "bottomright":
                parts.append(rect(wx1 - B, sy, B, B, TITLE))
            out.append('<g id="%s-%s">%s</g>' % (prefix, name, "".join(parts)))
    return out, W, H


def flat_set(prefix, ox, oy):
    """Maximized frame: square, no shadow. Only -center is drawn by Aurorae."""
    T = 4
    cols = [(ox, T), (ox + T, EDGE), (ox + T + EDGE, T)]
    rows = [(oy, T), (oy + T, EDGE), (oy + T + EDGE, T)]
    names = [["topleft", "top", "topright"], ["left", "center", "right"], ["bottomleft", "bottom", "bottomright"]]
    out = []
    for j, (sy, sh) in enumerate(rows):
        for i, (sx, sw) in enumerate(cols):
            out.append('<g id="%s-%s">%s</g>' % (prefix, names[j][i], rect(sx, sy, sw, sh, TITLE)))
    return out, 2 * T + EDGE, 2 * T + EDGE


def decoration_svg():
    defs, body = [], []
    x = 0
    maxh = 0
    for prefix, a0 in (("decoration", 0.50), ("decoration-inactive", 0.32)):
        els, w, h = frame_set(defs, prefix, x, 0, a0)
        body += els
        x += w + 10
        maxh = max(maxh, h)
    for prefix in ("decoration-maximized", "decoration-maximized-inactive"):
        els, w, h = flat_set(prefix, x, 0)
        body += els
        x += w + 10
    # stretch edges instead of tiling them (they are uniform along their length)
    body.append('<g id="hint-stretch-borders">%s</g>' % rect(x, 0, 2, 2, "#000000", ' fill-opacity="0"'))
    x += 2
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
            '<defs>\n%s\n</defs>\n%s\n</svg>\n') % (x, maxh, x, maxh, "\n".join(defs), "\n".join(body))


# ---- buttons -------------------------------------------------------------
BW, BH = 30, 36
# dot origins on the 10x10 cell (xfwm: dots at x 11-13 / 16-18, y 14-16 / 19-21)
DOT = {"tl": (11, 14), "tr": (16, 14), "bl": (11, 19), "br": (16, 19)}

BUTTONS = {
    # name: (dots, active colour)
    "close": (("tl", "tr", "bl", "br"), "#e06e6e"),
    "maximize": (("tl", "tr", "br"), "#8ccf7e"),
    "restore": (("tl", "bl", "br"), "#8ccf7e"),
    "minimize": (("bl",), "#e5c76b"),
    # extras, same language
    "alldesktops": (("tl", "br"), "#c47fd5"),
    "keepabove": (("tl", "tr"), "#67b0e8"),
    "keepbelow": (("bl", "br"), "#67b0e8"),
    "shade": (("tl", "tr", "bl"), "#6da4cd"),
    "help": (("tr", "bl"), "#6da4cd"),
}


def hover_box(ox, fill):
    # xfwm prelight: 24x24 square at x3..26, y6..29 with 1px clipped corners
    return rect(ox + 3, 7, 24, 22, fill) + rect(ox + 4, 6, 22, 24, fill)


def button_svg(dots, color):
    # (state prefix, background box, glyph colour, glyph opacity)
    states = [
        ("active", None, color, 1),
        ("hover", HOVER, color, 1),
        ("pressed", PRESS, color, 1),
        ("deactivated", None, color, 0.35),
        ("inactive", None, INACT, 1),
        ("hover-inactive", HOVER, color, 1),     # xfwm shows the prelight image on unfocused windows too
        ("pressed-inactive", PRESS, color, 1),
        ("deactivated-inactive", None, INACT, 0.3),
    ]
    groups = []
    for i, (st, box, col, op) in enumerate(states):
        ox = i * BW
        parts = [rect(ox, 0, BW, BH, TITLE)]
        if box:
            parts.append(hover_box(ox, box))
        extra = ' fill-opacity="%s"' % fmt(op) if op != 1 else ""
        parts += [rect(ox + DOT[d][0], DOT[d][1], 3, 3, col, extra) for d in dots]
        groups.append('<g id="%s-center">%s</g>' % (st, "".join(parts)))
    w = BW * len(states)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" shape-rendering="crispEdges">\n%s\n</svg>\n'
            % (w, BH, w, BH, "\n".join(groups)))


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "decoration.svg"), "w") as f:
        f.write(decoration_svg())
    for name, (dots, color) in BUTTONS.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(button_svg(dots, color))


if __name__ == "__main__":
    main()
