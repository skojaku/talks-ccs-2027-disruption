"""After the failure of the D-index: what it does, in plain words and with one graph; that papers do not sort cleanly; then let
the colours mix smoothly and spread (continuity), ending with the thesis sentence. The graph keeps one place on all four slides."""
from mm import *  # noqa: F401,F403
import mm
import s_dindex as D

CX, CY, K = 1000, 690, 1.3                  # where the graph sits, on all four slides
RED, BLUE = (177, 68, 52), (57, 89, 166)


def blend(t, white=0.0):
    """t = 0 red ('cites the focal paper and its references') ... t = 1 blue ('cites the focal paper only'); white lightens."""
    c = [RED[i] + (BLUE[i] - RED[i]) * t for i in range(3)]
    c = [v + (255 - v) * white for v in c]
    return "#%02X%02X%02X" % tuple(round(v) for v in c)


GRAD = "linear-gradient(135deg,#B14434,#3959A6)"
GRAD_G = "linear-gradient(135deg,#4d4d4d,#B14434)"
PURPLE = "#754E6D"


def smooth(pos):
    """Colour every node by where it sits: red on the left, blue on the right, with a continuous change between."""
    xs = [x for nid, (x, y) in pos.items() if nid != "F"]
    lo, hi = min(xs), max(xs)
    t = lambda x: (x - lo) / (hi - lo)
    fills = {nid: blend(t(x), 0.0 if not nid.startswith("r") else 0.55) for nid, (x, y) in pos.items() if nid != "F"}
    fills["F"] = blend(t(pos["F"][0]), 0.0)
    return fills, t


OUTER = [  # (dx, dy) from the focal paper in the diagram's own units, the node it hangs on
    (-300, -330, "j"), (110, -340, "i"), (310, -250, "g2"), (330, -70, "p2"),
    (-370, -170, "k"), (-300, 250, "r0"), (-60, 290, "r1"), (260, 270, "r2")]


def build(add):
    pos = D.node_pos("mix", CX, CY, K)
    N = lambda nid: pos[nid]
    roles = lambda: [
        text("rr", "cites the focal paper<br>and its references", 400, 330, 38, "", HOT, weight=700, w=700, h=170),
        overlay_svg("rra", [arrow_px(560 * S, 400 * S, N("j")[0] * S - 38, N("j")[1] * S - 8, HOT, 4, 16)]),
        text("rb", "cites the focal<br>paper only", 1700, 330, 38, "", COOL, weight=700, w=700, h=170),
        overlay_svg("rba", [arrow_px(1560 * S, 395 * S, N("i")[0] * S + 38, N("i")[1] * S - 8, COOL, 4, 16)]),
        text("rg", "cites the references<br>only", 470, 780, 38, "", GRAYC, weight=700, w=700, h=170),
        overlay_svg("rga", [arrow_px(640 * S, 740 * S, N("k")[0] * S - 36, N("k")[1] * S + 14, GRAYC, 4, 16)])]
    graph = lambda fills=None, ecol=None: D.diagram("mix", "mix", CX, CY, K, labels=False, fills=fills, ecol=ecol)

    # 1  what the D-index does, in plain words: one graph, the colour roles written on it
    add(h2("D-index sorts the citing papers") + '\n\n<p class="sub">Do they cite the focal paper, the work before it, or both?</p>'
        + stage(*graph(), *roles()), cls="L-b")

    # 2  ... but papers do not sort so cleanly: some belong to two groups at once
    mixed = {"p2": GRAD, "a": GRAD, "k": GRAD_G}
    emix = {"p2": PURPLE, "a": PURPLE, "k": "#7A4A40"}
    add(h2("But papers do not sort so cleanly") + stage(
        *graph(mixed, emix), *roles(),
        text("as1", "Some belong to<br>two groups at once.", 1600, 760, 44, "aside", w=800, h=190),
        overlay_svg("as1ar", [curved_arrow(1450 * S, 740 * S, N("p2")[0] * S + 40, N("p2")[1] * S + 18, 0.25, MUTED, 3, 16)])), cls="L-b")

    # 3  stop sorting: the colours change smoothly from one paper to the next, in the same place
    fills, t = smooth(pos)
    add(h2("Stop sorting. Let the colours mix.") + stage(*graph(fills, fills)), cls="L-b")

    # 4  ... and the mixture spreads outwards, still smooth
    o = []
    for n, (dx, dy, host) in enumerate(OUTER):
        x, y = CX + K * dx, CY + K * dy
        tt = min(1.0, max(0.0, t(x)))
        col = blend(tt)
        x1, y1, x2, y2 = trim(*pos[host], x, y, 32, 28)
        o.append(line(f"mix_o{n}e", x1, y1, x2, y2, col, 3, False))
        o.append(sq(f"mix_o{n}", x, y, 46, col))
    add(h2("The mixture spreads") + stage(*graph(fills, fills), *o), cls="L-b")

    # 5  the thesis, in words only
    add(h2('We preserve <span class="hot">continuity</span> by abandoning class rounding.'), cls="L-f", header="")
