#!/usr/bin/env python3
"""Compare element IDs of the Everblush desktoptheme SVGs with Breeze's.

Usage: python3 check-ids.py [breeze_dir]   (default /usr/share/plasma/desktoptheme/default)
Reports, per file, Breeze IDs missing from ours (ignoring Inkscape/auto IDs).
"""
import gzip, os, re, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OURS = os.path.join(HERE, "desktoptheme", "Everblush")
BREEZE = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/plasma/desktoptheme/default"
AUTO = re.compile(r"^(path|rect|g|use|stop|layer|ellipse|circle|text|tspan|image|svg|defs|metadata|namedview|grid|"
                  r"guide|filter|feGaussianBlur|clipPath|linearGradient|radialGradient|perspective|pattern|polygon|"
                  r"polyline|line|mask)\d[\w.-]*$")
SKIP_TAGS = {"stop", "linearGradient", "radialGradient", "namedview", "grid", "metadata", "defs", "filter",
             "feGaussianBlur", "tspan", "text", "svg", "style", "pattern", "guide"}
# helper-only IDs Breeze uses internally (gradient helpers / sub-shapes), not looked up by Plasma
INTERNAL = {"shadow-side", "shadow-corner", "st", "sb", "sl", "sr", "msc", "pc", "a", "b", "c", "d", "e",
            "base", "shadow", "Checkerboard", "border-bottomleft"}


def ids(path):
    opener = gzip.open if path.endswith(".svgz") else open
    with opener(path, "rb") as fh:
        root = ET.parse(fh).getroot()
    out = set()
    for e in root.iter():
        i = e.get("id")
        tag = e.tag.split("}")[-1]
        if i and not AUTO.match(i) and tag not in SKIP_TAGS and not re.search(r"-\d+$", i):
            out.add(i)
    return out


bad = 0
for dp, _, files in os.walk(OURS):
    for fn in sorted(files):
        if not fn.endswith(".svg"):
            continue
        ours = os.path.join(dp, fn)
        rel = os.path.relpath(ours, OURS)
        ref = os.path.join(BREEZE, rel[:-4] + ".svgz")
        if not os.path.exists(ref):
            ref = os.path.join(BREEZE, rel)
        mine = ids(ours)
        if not os.path.exists(ref):
            print("%-36s no Breeze counterpart (%d ids)" % (rel, len(mine)))
            continue
        theirs = ids(ref) - INTERNAL
        missing = sorted(theirs - mine)
        extra = sorted(mine - theirs - INTERNAL)
        print("%-36s breeze=%3d ours=%3d missing=%d" % (rel, len(theirs), len(mine), len(missing)))
        if missing:
            bad += 1
            print("    MISSING:", " ".join(missing))
        if extra:
            print("    extra  :", " ".join(extra))
sys.exit(1 if bad else 0)
