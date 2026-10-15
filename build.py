#!/usr/bin/env python3
"""Build ccs-2027.md (a Marp deck) from the slide modules, check the morph names, and render it.

    python3 build.py            # write ccs-2027.md
    python3 build.py --html     # also write ccs-2027.html (the magic-move build; open it in Chrome)

The deck is the Keynote talk `ccs-2027.key`, rebuilt in the house style (HOUSE_STYLE.md). Objects that move
between slides in Keynote's Magic Move carry the same `view-transition-name` on both slides, so Marp's HTML
export (Chrome / Edge) moves them too; the PDF and PNG exports show each slide's final state.
"""
import re
import subprocess
import sys
from pathlib import Path

import mm
import s_hook

ROOT = Path(__file__).resolve().parent
SLIDES = []

FRONT = """---
marp: true
theme: house
paginate: true
math: katex
html: true
---
"""


def add(body, cls="L-g", header=None, notes=None, bg=None, trans=None):
    SLIDES.append(dict(body=body, cls=cls, header=header, notes=notes, bg=bg, trans=trans, names=mm.take_names()))


TAG = re.compile(r'<(\w+)[^>]*?style="([^"]*?view-transition-name:(\w+);?[^"]*)"')


def geometry(body):
    """name -> its inline style without the name: what decides whether the box moves, resizes or recolours."""
    out = {}
    for _, st, name in TAG.findall(body):
        out[name] = re.sub(r"view-transition-name:\w+;?", "", st)
    return out


def modules():
    mods = [s_hook]
    for name in ("s_dindex", "s_w2v", "s_walk", "s_end"):
        if (ROOT / f"{name}.py").exists():
            mods.append(__import__(name))
    return mods


def main():
    for m in modules():
        m.build(add)
    out = [None]
    header = None
    prev = set()
    prev_geo = {}
    report = []
    for i, s in enumerate(SLIDES, 1):
        names = s["names"]
        dup = {n for n in names if names.count(n) > 1}
        assert not dup, f"slide {i}: view-transition-name used twice: {sorted(dup)}"
        geo = geometry(s["body"])
        shared = prev & set(names)
        moving = {n for n in shared if geo.get(n) != prev_geo.get(n)}
        s["shared"] = len(moving)
        report.append((i, len(names), len(moving)))
        prev = set(names)
        prev_geo = geo
        head = []
        if s["cls"]:
            head.append(f"<!-- _class: {s['cls']} -->")
        if s["header"] is not None and s["header"] != header:
            header = s["header"]
            head.append(f'<!-- header: "{header}" -->')
        if s["bg"]:
            head.append(f"<!-- _backgroundColor: {s['bg']} -->")
        if moving and s["trans"] is not False:
            head.append("<!-- _transition: fade 1.1s -->")
        body = s["body"]
        notes = f"\n\n<!--\n{s['notes']}\n-->" if s["notes"] else ""
        out.append("\n".join(head) + "\n\n" + body + notes)
    (ROOT / "ccs-2027.md").write_text(FRONT + "\n" + "\n\n---\n\n".join(out[1:]) + "\n")
    if mm.RAISED:
        print("raised to the 30px floor:", sorted(set(mm.RAISED)))
    print(f"{len(SLIDES)} slides; morph pairs (slide, objects, shared with previous):")
    print("  " + "  ".join(f"{i}:{n}/{sh}" for i, n, sh in report))
    if "--html" in sys.argv:
        subprocess.run(["marp", "--no-stdin", "--html", "--theme-set", "theme.css", "--allow-local-files",
                        "ccs-2027.md", "-o", "ccs-2027.html"], check=True, cwd=ROOT)
        print("wrote ccs-2027.html")


if __name__ == "__main__":
    main()
