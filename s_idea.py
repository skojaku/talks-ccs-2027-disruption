"""The big picture between the failure of the D-index and word2vec: look wider, find the bottleneck, sample paths,
let word2vec turn the pairs into coordinates."""
import math
import random

from mm import *  # noqa: F401,F403
import mm
from s_walk import PAIRS, SEQ, pair
from s_w2v import net


def sqn(name, x, y, s, fill, ring=None):
    return sq(name, x, y, s, fill, ring, 2)


def ring_graph(step):
    """A focal paper with the papers 1 step away (lit) and 2 steps away (pale); step 2 adds the links among neighbours."""
    cx, cy = 1000, 650
    rg = random.Random(11)
    r1 = [(cx + 230 * math.cos(math.radians(a)), cy + 230 * math.sin(math.radians(a))) for a in range(15, 360, 60)]
    r2 = [(cx + 430 * math.cos(math.radians(a + rg.uniform(-6, 6))), cy + 430 * math.sin(math.radians(a + rg.uniform(-6, 6))))
          for a in range(0, 360, 30)]
    o = []
    # 2-step papers hang on their nearest 1-step paper (pale edges)
    for i, p in enumerate(r2):
        j = min(range(6), key=lambda t: (r1[t][0] - p[0]) ** 2 + (r1[t][1] - p[1]) ** 2)
        x1, y1, x2, y2 = trim(*r1[j], *p, 30, 30)
        o.append(line(f"r2e{i}", x1, y1, x2, y2, PALE, 3, False))
    for i, p in enumerate(r1):
        x1, y1, x2, y2 = trim(*p, cx, cy, 30, 48)
        o.append(line(f"r1e{i}", x1, y1, x2, y2, INK, 4.5, True, False, 16))
    if step >= 2:
        for i in range(6):
            x1, y1, x2, y2 = trim(*r1[i], *r1[(i + 1) % 6], 34, 34)
            if i in (0, 2, 3, 5):
                o.append(line(f"nn{i}", x1, y1, x2, y2, HOT, 5, True, True, 18))
    for i, p in enumerate(r2):
        o.append(sqn(f"r2s{i}", *p, 46, FAINT))
    for i, p in enumerate(r1):
        o.append(sqn(f"r1s{i}", *p, 62, COOL))
    o.append(dia("focal", cx, cy, 96, DEEP))
    o.append(text("l1", "1 step", cx + 285, cy - 215, 40, "", INK, weight=700, w=300, align="left"))
    o.append(text("l2", "2 steps", cx + 470, cy - 380, 40, "", MUTED, w=300, align="left"))
    return o


def hourglass():
    """Ancestors below, descendants above, the focal paper at the narrow waist."""
    rg = random.Random(3)
    rows = [(330, 8), (480, 6), (610, 3), (760, 1), (910, 3), (1040, 6)]
    cx, wide = 1000, 1050
    pos = []
    for y, n in rows:
        w = wide * (0.28 + 0.72 * (n - 1) / 7) if n > 1 else 0
        xs = [cx - w / 2 + w * (i / (n - 1)) for i in range(n)] if n > 1 else [cx]
        pos.append([(x + rg.uniform(-18, 18), y) for x in xs])
    o = []
    for r in range(len(rows) - 1):
        for i, a in enumerate(pos[r]):
            for j, b in enumerate(pos[r + 1]):
                near = abs(i / max(1, len(pos[r]) - 1) - j / max(1, len(pos[r + 1]) - 1)) < 0.5
                if near or rg.random() < 0.15:
                    x1, y1, x2, y2 = trim(*a, *b, 26, 26)
                    o.append(line(f"hg{r}_{i}_{j}", x1, y1, x2, y2, MUTED, 2.6, True, False, 11))
    for r, ps in enumerate(pos):
        for i, p in enumerate(ps):
            if rows[r][1] == 1:
                o.append(dia("hg_focal", *p, 84, DEEP))
            else:
                o.append(sqn(f"hg_s{r}_{i}", *p, 44, PALE if rows[r][0] > 760 else COOL))
    o.append(box("waist", 700, 690, 600, 140, "", "", f"border:4px dashed {HOT};border-radius:70px;"))
    o.append(text("bn", "bottleneck", 1380, 760, 56, "", HOT, weight=700, w=700, align="left"))
    o.append(overlay_svg("bn_ar", [arrow_px(1360 * S, 760 * S, 1315 * S, 762 * S, HOT, 5, 20)]))
    o.append(text("later", "later work", 1660, 330, 36, "", MUTED, w=500, align="left"))
    o.append(text("earlier", "earlier work", 1660, 1040, 36, "", MUTED, w=500, align="left"))
    o.append(overlay_svg("flow", [arrow_px(150 * S, 1040 * S, 150 * S, 330 * S, MUTED, 4, 22)]))
    return o


def build(add):
    # ---- the D-index sees only close neighbours -----------------------------------------------------------------------------
    T = h2("D-index sees only close neighbours")
    add(T + stage(*ring_graph(1)), cls="L-b")
    add(T + stage(*ring_graph(2), text("as1", "How the neighbours<br>connect is ignored.", 330, 300, 44, "aside", w=700, h=190)), cls="L-b")

    # ---- our idea: zoom out and find the bottleneck of the flow ------------------------------------------------------------------
    add(h2("Zoom out: find the bottleneck") + '\n\n<p class="sub">of how knowledge builds up</p>' + stage(*hourglass()), cls="L-b")

    # ---- word2vec as an information compressor: pairs in, coordinates out ------------------------------------------------------------
    rows = [(0, 360), (1, 540), (4, 720), (6, 900)]
    pts = [(1560, 520, SEQ[0]), (1700, 640, SEQ[1]), (1830, 540, SEQ[2]), (1640, 780, SEQ[3]), (1790, 800, SEQ[4]), (1520, 700, SEQ[5])]
    add(h2("word2vec turns pairs into coordinates") + stage(
        text("pl", "(ancestor, descendant)", 400, 250, 36, "", INK, w=800),
        *[pair(f"ip{i}", k, 380, y, 88) for i, (k, y) in enumerate(rows)],
        line("ia1", 540, 640, 700, 640, INK, 4, True, False, 20),
        net("inet", 1010, 650, 0.85),
        text("inl", "word2vec", 1010, 340, 48, "", INK, weight=700, w=700),
        text("ins", "an information compressor", 1010, 1000, 40, "aside", w=900),
        line("ia2", 1250, 640, 1440, 640, INK, 4, True, False, 20),
        line("sx", 1470, 860, 1900, 860, INK, 3.4, True, False, 16), line("sy", 1470, 860, 1470, 420, INK, 3.4, True, False, 16),
        *[disc(f"id{i}", x, y, 56, c, RING_, 3.5) for i, (x, y, c) in enumerate(pts)],
        text("itx", "a coordinate per node", 1650, 950, 36, "", INK, w=800)), cls="L-b")

    # ---- ... and simple linear algebra measures how nodes relate --------------------------------------------------------------
    ox, oy = 700, 900
    q_end, k_end = (1250, 420), (1500, 760)
    add(h2("Simple linear algebra measures relations") + stage(
        line("la_x", ox - 100, oy, 1800, oy, "#B3B3B3", 3, True, False, 16), line("la_y", ox, oy + 80, ox, 330, "#B3B3B3", 3, True, False, 16),
        line("la_q", ox, oy, *q_end, HOT, 7, True, False, 26), line("la_k", ox, oy, *k_end, COOL, 7, True, False, 26),
        text("la_ql", "query", q_end[0] + 40, q_end[1] - 50, 44, "", HOT, weight=700, w=500, align="left"),
        text("la_kl", "key", k_end[0] + 40, k_end[1] + 10, 44, "", COOL, weight=700, w=500, align="left"),
        text("la_t", "angle", 1130, 745, 40, "aside", w=500),
        mathbox("la_m", 1290, 905, 600, 160, "$$\\cos\\theta,\\ \\ \\lVert q-k\\rVert$$", 52)), cls="L-b")


RING_ = "#4d4d4d"
