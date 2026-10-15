"""After the failure of the D-index: what it does in plain words, why papers do not sort so cleanly, then let the colours mix
and spread (continuity), ending with the thesis sentence."""
from mm import *  # noqa: F401,F403
import mm
import s_dindex as D


def blend(t):
    """t = 0 is the red of 'cites the focal paper and its references', t = 1 the blue of 'cites the focal paper only'."""
    a, b = (177, 68, 52), (57, 89, 166)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


GRAD = "linear-gradient(135deg,#B14434,#3959A6)"
GRAD_G = "linear-gradient(135deg,#4d4d4d,#B14434)"
PURPLE = "#754E6D"
# every node gets its own mixture once the groups are dropped (p2, a, j, i, k, g2 of the 'mix' diagram)
MIXED = {"j": blend(.15), "a": blend(.6), "i": blend(.85), "p2": blend(.4), "k": "#6A4E55", "g2": "#555A78"}
OUTER = [  # (dx, dy) from the focal paper in the diagram's own units, the node it hangs on, the mixture
    (-300, -340, "j", .1), (110, -350, "i", .8), (310, -250, "g2", .55), (330, -70, "p2", .3),
    (-370, -170, "k", .35), (-300, 270, "r0", .2), (-60, 340, "r1", .5), (260, 300, "r2", .7)]


def outer(pre, cx, cy, k, pos):
    o = []
    for n, (dx, dy, host, t) in enumerate(OUTER):
        x, y = cx + k * dx, cy + k * dy
        x1, y1, x2, y2 = trim(*pos[host], x, y, 32, 28)
        o.append(line(f"{pre}_o{n}e", x1, y1, x2, y2, blend(t), 3, False))
        o.append(sq(f"{pre}_o{n}", x, y, 46, blend(t)))
    return o


def build(add):
    BOXES = (D.CITE_TOP, D.CITE_REF, D.CITE_REF)
    DX, DY = 472, 690                    # the figure of the "decision tree" slide, a little lower for the title
    fig = lambda fills=None, ecol=None, sq_=D.SQ_CONCEPT: [
        *D.diagram("mix", "mix", DX, DY, 1.0, labels=True, fills=fills, ecol=ecol),
        *D.tree("t", 1466, 340, 1.0, "concept", BOXES, sq_, captions=True)]

    # 1  what the D-index does, in plain words
    add(h2("D-index sorts the citing papers") + '\n\n<p class="sub">Do they cite the focal paper, the work before it, or both?</p>'
        + stage(*fig()), cls="L-b")

    # 2  ... but papers do not sort so cleanly: some belong to two groups at once
    mixed = {"p2": GRAD, "a": GRAD, "k": GRAD_G}
    emix = {"p2": PURPLE, "a": PURPLE, "k": "#7A4A40"}
    straddle = [("s0", 0, 5, -50, HOT, None), ("s1", 0, 105, 23, GRAD, None), ("s2", 1, -108, -35, GRAD, None),
                ("s3", 1, 20, 40, TEAL, None), ("s4", 2, 0, 3, GRAYC, None)]
    add(h2("But papers do not sort so cleanly") + stage(
        *fig(mixed, emix, straddle),
        text("as1", "Some belong to<br>two groups at once.", 330, 262, 44, "aside", w=700, h=190)), cls="L-b")

    # 3  stop sorting: the boxes go, the colours stay and mix
    pos3 = D.node_pos("mix", 1000, 640, 1.3)
    add(h2("Stop sorting. Let the colours mix.") + stage(
        box("glow", 1000 - 560, 640 - 560, 1120, 1120, "", "",
            f"border-radius:50%;background:radial-gradient(circle,rgba(117,78,109,.30),rgba(117,78,109,0) 68%);"),
        *D.diagram("mix", "mix", 1000, 640, 1.3, labels=False, fills=MIXED, ecol=MIXED)), cls="L-b")

    # 4  ... and the mixture spreads outwards
    add(h2("The mixture spreads") + stage(
        box("glow", 1000 - 840, 640 - 840, 1680, 1680, "", "",
            f"border-radius:50%;background:radial-gradient(circle,rgba(117,78,109,.30),rgba(117,78,109,0) 68%);"),
        *D.diagram("mix", "mix", 1000, 640, 1.3, labels=False, fills=MIXED, ecol=MIXED),
        *outer("mix", 1000, 640, 1.3, pos3)), cls="L-b")

    # 5  the thesis, in words only
    add(h2('We preserve <span class="hot">continuity</span> by abandoning class rounding.'), cls="L-f", header="")
