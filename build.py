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


LABELS = [
    (r"^(edison|lbt|lbaside)$", "Edison photo"), (r"^(phone|chat|globe|printer)$", "technology pictures"),
    (r"^(adams)$", "Douglas Adams portrait"), (r"^(tl|tl2|tl_[lmr])$", "timeline"), (r"^(age\d)$", "age labels"),
    (r"^(era\d|as\d|ar\d)$", "era labels and notes"), (r"^(pager|nokia\w*|glasses|flip|iphone|docomo)$", "phone pictures"),
    (r"^(bohr|vegard|schrod|cap\d)$", "atomic-model pictures"), (r"^(dev|dis|mix)_", "citation diagram"),
    (r"^(tdev|tdis|dv\d)$", "diagram labels"), (r"^(see_[lr]|fulcrum)$", "seesaw"), (r"^t_", "decision tree"),
    (r"^(fml|fcard|fu\d|fk\d|counts|counts_ar|recap)$", "formula"), (r"^(p_team|p_trend|p_remote|c_team|c_trend|c_remote)$", "the three papers"),
    (r"^hphoto$", "Higgs photo"), (r"^(an\d.*|hd_.*)$", "annotations"), (r"^hn_", "Higgs citation network"),
    (r"^(hl\d|hd\d)$", "network labels"), (r"^(ax_.*|ay\d|ax\d|step|smooth|lbl_[de])$", "plot axes and curves"), (r"^net$", "neural network drawing"),
    (r"^(fx|fxv|fx_ar)$", "fox example"), (r"^(m1|m2)$", "metonymy text"), (r"^an_\w$", "analogy equations"), (r"^(sent|sent_ar|lf|lp|lf2|foot)$", "sentence and word labels"),
    (r"^(qv|kv|kv2|qm|km|qn\d|kn\d|qu|ku|ql|kl|bq|bk)$", "query and key vectors"), (r"^d_", "embedding dots"), (r"^(kl\d|ql\d|wl\d|wl_ar|rj|ls|ls_ar)$", "dot labels"),
    (r"^(mv\d)$", "movement arrows"), (r"^(w_.*|wbrush|rw)$", "random-walk tree"), (r"^s\d$", "sequence discs"), (r"^(win|arcs|winl|qk|tdlab)$", "window and labels"),
    (r"^pr\d$", "training pairs"), (r"^(lh|as1.*|as2.*)$", "list heading and notes"), (r"^(sg\d|st|so|sk|sq|sb|sd|fp|tk)$", "embedding scatter"),
    (r"^(ar\d|na\d|ma\d|nkl|nql|mkl|mql)$", "arrows"), (r"^(av|bf|qr2|c\d|paperimg|papercap|paperlead|qrpaper|qrcap)$", "contact and paper"),
]


def describe(names):
    import re as _re
    out = []
    for n in sorted(names):
        for pat, lab in LABELS:
            if _re.search(pat, n):
                if lab not in out:
                    out.append(lab)
                break
        else:
            if n not in out:
                out.append(n)
    return out


# Choices made on the "遷移の指定" page (slide numbers as they were before the opening slide was added: +1 now).
CUT = {n + 1 for n in (11, 12, 13, 14, 58)}      # hard cuts: nothing glides or fades
MORPH = set()


def modules():
    import s_hook, s_dindex, s_mix, s_idea, s_walk, s_w2v, s_end
    return [s_hook.build, s_dindex.build, s_mix.build, s_walk.build_a1, s_idea.compressor, s_w2v.build, s_idea.compressor,
            s_walk.build_a2, s_idea.onepaper, s_walk.focus, s_walk.build_b, s_end.build]


def main():
    for m in modules():
        m(add)
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
        prev_names = prev
        prev_names_ = set(prev)
        moving = {n for n in shared if geo.get(n) != prev_geo.get(n)}
        s["shared"] = len(moving)
        s["moving"] = sorted(moving)
        s["appear"] = sorted(set(names) - prev)
        s["vanish"] = sorted(prev - set(names))
        report.append((i, len(names), len(moving)))
        prev = set(names)
        prev_geo = geo
        if shared:                                   # a build step: arrows that are new on it grow from their base
            def mark(m):
                return m.group(0) if m.group(3) in prev_names else m.group(1) + " grow" + m.group(2)
            s["body"] = re.sub(r'(<div class="o (?:ln|ov)[^"]*?)(" style="[^"]*?view-transition-name:(\w+))', mark, s["body"])
        head = []
        if s["cls"]:
            head.append(f"<!-- _class: {s['cls']} -->")
        # (no breadcrumb header: the lecturer removed it from every slide)
        if s["bg"]:
            head.append(f"<!-- _backgroundColor: {s['bg']} -->")
        if i in CUT:
            moving = set()
            s["shared"] = 0
        if (moving or i in MORPH) and s["trans"] is not False:
            head.append("<!-- _transition: fade 1.1s -->")
        body = s["body"]
        notes = f"\n\n<!--\n{s['notes']}\n-->" if s["notes"] else ""
        out.append("\n".join(head) + "\n\n" + body + notes)
    (ROOT / "ccs-2027.md").write_text(FRONT + "\n" + "\n\n---\n\n".join(out[1:]) + "\n")
    import json, re as _re2
    dump = []
    for i, s in enumerate(SLIDES, 1):
        t = _re2.search(r"<h2[^>]*>(.*?)</h2>", s["body"], _re2.S)
        title = _re2.sub(r"<[^>]+>", "", t.group(1)).strip() if t else ""
        if not title:
            tx = _re2.search(r'class="o tx[^"]*"[^>]*>(?:<span>)?(.*?)</', s["body"], _re2.S)
            title = _re2.sub(r"<[^>]+>", " ", tx.group(1)).strip() if tx else ""
        import html as _html
        title = _html.unescape(title)
        dump.append(dict(n=i, title=title, content=describe(s["names"])[:5], layout=s["cls"], moving=describe(s.get("moving", [])), n_moving=s.get("shared", 0),
                         appear=describe(s.get("appear", [])), vanish=describe(s.get("vanish", [])),
                         grows=("grow" in s["body"]), fragments=len(_re2.findall(r"^\s*\* ", s["body"], _re2.M)),
                         transition="magic move" if s.get("shared") and s["trans"] is not False else "cut"))
    (ROOT / "review" / "transitions.json").write_text(json.dumps(dump, ensure_ascii=False, indent=1))
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
