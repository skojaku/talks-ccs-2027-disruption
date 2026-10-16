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
    # the roles, written beside a square of each kind: plain words, no underline, no arrows
    def roles(mute=False):
        col = (lambda c: MUTED) if mute else (lambda c: c)
        sty = 'style="background:none;padding:0"'
        return [
            text("rr", "build on prior + focal", N("j")[0] - 40, N("j")[1] - 42, 38, "", col(HOT), w=700, align="right", style="font-weight:700;"),
            text("rb", "build on focal", N("i")[0] + 50, N("i")[1] - 42, 38, "", col(COOL), w=500, align="left", style="font-weight:700;"),
            text("rg", "build on prior", N("k")[0] - 34, N("k")[1] + 6, 38, "", col(GRAYC), w=500, align="right", style="font-weight:700;")]
    graph = lambda fills=None, ecol=None: D.diagram("mix", "mix", CX, CY, K, labels=False, fills=fills, ecol=ecol)

    # 1  what the D-index does, in plain words: one graph, the colour roles written on it
    add(h2("D-index sorts the citing papers") + '\n\n<p class="sub">Does a paper build on the focal paper, the work before it, or both?</p>'
        + stage(*graph(), *roles()), cls="L-b")

    # 2  ... but papers do not sort so cleanly: the one sentence that matters, large, above the graph; nothing else
    mixed = {"p2": GRAD, "a": GRAD, "k": GRAD_G}
    emix = {"p2": PURPLE, "a": PURPLE, "k": "#7A4A40"}
    add(h2("But papers do not sort so cleanly") + stage(
        *graph(mixed, emix),
        text("as1", "Some belong to two groups at once.", 960, 270, 52, "aside", w=1500, h=120,
             style="background:linear-gradient(90deg,#B14434,#3959A6);-webkit-background-clip:text;background-clip:text;"
                   "color:transparent;")), cls="L-b")

    # 5  the thesis, in words only
    add(h2('We preserve <span class="hot">continuity</span> by abandoning class rounding.'), cls="L-f", header="")
