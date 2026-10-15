"""Slides 70-81: the measure, the test, the results, the summary and the contact slide."""
from mm import *  # noqa: F401,F403
import mm
from s_walk import STATES, GRAYP, RING


def scatter_thumb(cx, cy, k):
    """The 'split' scene of the embedding space, unnamed and scaled, for the summary."""
    st = STATES["split"]
    P = lambda p: (cx + (p[0] - 1060) * k, cy + (p[1] - 700) * k)
    d = 80 * k
    o = []
    for p in st["gray"]:
        o.append(disc(None, *P(p), d, FAINT, GRAYP, 2))
    for key, col, dash, op in (("teal", TEAL, False, .55), ("olive", OLIVE, False, .55), ("lb", COOL, True, .55),
                               ("db", DEEP, True, .55), ("fk", HOT, True, 1), ("fq", HOT, False, 1)):
        o.append(disc(None, *P(st[key]), d, col, RING, 2.4, dashed=dash, opacity=op))
    return o


def build(add):
    # ---- 70  the measure ----------------------------------------------------------------------------------------------
    A = lambda x1, y1, x2, y2, bend: overlay_svg(None, [curved_arrow(x1 * S, y1 * S, x2 * S, y2 * S, bend, HOT, 6, 24)])
    add(h2("Embedding Disruptiveness Measure (EDM)") + stage(
        mathbox("edm", 300, 330, 1440, 220, "$$\\Delta_i := 1-\\cos(q_i,k_i)$$", 60),
        text("edmn", "Dissimilarity of the descendants<br>and ascendants of node i.", 1545, 598, 32, "aside", w=900, h=170),
        img("hphoto", "assets/higgs.jpg", 935, 872, 620, None, "ph"),
        text("e1", "Δ = 1.002<br>Top 4.3 %", 305, 890, 44, "", HOT, w=620, h=170),
        text("e2", "Δ = 1.005<br>Top 4.1 %", 1640, 960, 44, "", HOT, w=620, h=170),
        overlay_svg("e_ar", [curved_arrow(465 * S, 770 * S, 715 * S, 818 * S, 0.3, HOT, 6, 24),
                             curved_arrow(1430 * S, 880 * S, 1235 * S, 836 * S, -0.3, HOT, 6, 24)])), cls="L-b", header="")

    # ---- 71  the test ------------------------------------------------------------------------------------------------
    add(h2("Does EDM beat the D-index? 🤔") + '\n\n<p class="sub">Tested with APS data</p>' + stage(
        img("aps1", "assets/aps_news.png", 535, 640, 860, None, "ph"),
        img("aps2", "assets/prl.png", 1484, 700, 812, 440, "ph top cover")), cls="L-a")

    # ---- 72  the null model -----------------------------------------------------------------------------------------------
    NODE = "#A6A6A6"
    ARW = "#333333"
    L = {"t": [(498, 660), (641, 660), (804, 660)], "m": [(463, 806), (716, 806)], "b": [(544, 925), (663, 925)]}
    R = {"t": [(1392, 645), (1536, 646), (1699, 646)], "m": [(1357, 792), (1610, 792)], "b": [(1438, 912), (1558, 912)]}

    def netw(pre, D, edges):
        o = []
        for i, (a, b) in enumerate(edges):
            pa = D[a[0]][a[1]]
            pb = D[b[0]][b[1]]
            x1, y1, x2, y2 = trim(*pa, *pb, 42, 46)
            o.append(line(f"{pre}e{i}", x1, y1, x2, y2, ARW, 4.2, True, False, 15))
        for k, row in D.items():
            for j, p in enumerate(row):
                o.append(disc(f"{pre}{k}{j}", *p, 76, NODE, None))
        return o

    add(h2("Conformal analysis") + '\n\n<p class="sub muted">Preserve degrees and time gap.<br>Shuffle everything else.</p>' + stage(
        *netw("L", L, [(("t", 0), ("m", 0)), (("t", 0), ("b", 1)), (("t", 1), ("m", 1)), (("t", 1), ("b", 0)), (("t", 2), ("m", 1))]),
        *netw("R", R, [(("t", 0), ("b", 0)), (("t", 0), ("m", 1)), (("t", 1), ("m", 0)), (("t", 1), ("b", 1)), (("t", 2), ("m", 1))]),
        text("n1", "original network", 663, 575, 32, "", MUTED, weight=700, w=900),
        text("n2", "random network", 1573, 572, 32, "", MUTED, weight=700, w=900),
        line("tm1", 297, 955, 297, 585, LAV, 6, True, False, 28), line("tm2", 1230, 955, 1230, 585, LAV, 6, True, False, 28),
        text("tl1", "Time", 245, 770, 28, "", LAV, weight=700, w=300, style="transform:rotate(-90deg);"),
        text("tl2", "Time", 1178, 770, 28, "", LAV, weight=700, w=300, style="transform:rotate(-90deg);")), cls="L-b")

    # ---- 73-75  the D-index: milestone papers sit at the bottom -------------------------------------------------------
    T1 = h2("D-index of milestone works (APS)")
    plot = lambda: img("histD", "assets/hist_dindex.png", 1020, 690, 1215)
    a1 = lambda: [text("a1", "Milestone papers with<br>the bottom-level<br>D-index value.", 270, 975, 32, "aside", w=700, h=230),
                  overlay_svg("a1ar", [curved_arrow(520 * S, 940 * S, 655 * S, 925 * S, -0.15, MUTED, 2.6, 15)])]
    a2 = lambda: [text("a2", "Shuffling creates<br>more high<br>D-index works 🙈", 1135, 690, 32, "aside", w=700, h=300),
                  overlay_svg("a2ar", [curved_arrow(1345 * S, 612 * S, 1490 * S, 578 * S, -0.2, MUTED, 2.6, 15)])]
    add(T1 + stage(plot()), cls="L-b")
    add(T1 + stage(plot(), *a1()), cls="L-b")
    add(T1 + stage(plot(), *a1(), *a2()), cls="L-b")

    # ---- 76-78  the EDM: milestone papers sit at the top ----------------------------------------------------------------
    def both():
        return [img("histD", "assets/hist_dindex.png", 400, 640, 490, None, "faded"),
                text("hd", "D-index", 390, 330, 40, "", MUTED, w=700),
                img("histE", "assets/hist_edm.png", 1425, 600, 1125),
                text("he", "EDM", 1548, 100, 64, "", HOT, w=700)]

    b1 = lambda: [text("b1", "Many milestone<br>papers have a high<br>EDM value", 1525, 490, 32, "aside", w=700, h=250),
                  overlay_svg("b1ar", [curved_arrow(1700 * S, 388 * S, 1862 * S, 325 * S, -0.15, MUTED, 2.6, 15)])]
    b2 = lambda: [text("b2", "Randomization<br>reduces the EDM-<br>score for most works", 615, 985, 32, "aside", w=800, h=250),
                  overlay_svg("b2ar", [curved_arrow(875 * S, 905 * S, 1035 * S, 858 * S, -0.2, MUTED, 2.6, 15)])]
    add(stage(*both()), cls="L-g")
    add(stage(*both(), *b1()), cls="L-g")
    add(stage(*both(), *b1(), *b2()), cls="L-g")

    # ---- 79  the result ------------------------------------------------------------------------------------------------------
    lab = lambda n, t, x, y, x2, y2: [text(n, t, x, y, 30, "", MUTED, w=700, style="font-style:italic;"),
                                       overlay_svg(n + "a", [curved_arrow(x2 * S - 120, y2 * S + 2, x2 * S, y2 * S, 0.05, MUTED, 2.6, 14)])]
    add(h2("EDM aligns better with human judgment") + stage(
        img("odds", "assets/odds_ratio.png", 1275, 650, 1240, None, "ph"),
        *lab("o1", "Control<br>variable", 180, 440, 655, 388), *lab("o2", "EDM<br>(proposed)", 290, 650, 672, 625),
        *lab("o3", "D-index", 320, 840, 682, 840),
        img("apsc", "assets/aps_news.png", 255, 1050, 440, None)), cls="L-b")

    # ---- 80-81  summary (left to me: "Summary" as F, then three claims, each with the picture that showed it) -------------
    add(h2("Summary"), cls="L-f", header="")
    def claim(n, y, head, sub):
        # one `*` item per claim: it appears on its own click, with its evidence line under it
        return (f'<div class="o blist" style="left:340px;top:{y}px;width:880px">\n\n'
                f'* <span class="claim">{head}</span><span class="sub2">{sub}</span>\n\n</div>')

    add(stage(
        img("sm1", "assets/higgs.jpg", 290, 270, 360, None, "ph"),
        claim("k1", 150, 'The D-index <span class="hot">fails</span> on milestone works', 'Higgs (1964): D = −0.27, Bottom 0.1 %'),
        *scatter_thumb(290, 600, 0.2),
        claim("k2", 310, 'EDM preserves <span class="hot">continuity</span>', 'A large query-key gap marks a discontinuity'),
        img("sm3", "assets/odds_ratio.png", 290, 905, 360, None, "ph"),
        claim("k3", 470, 'EDM matches <span class="hot">human judgment</span>', 'Odds ratio 1.23, against 1.03 for the D-index')),
        cls="L-g")

    # ---- 81  contact -------------------------------------------------------------------------------------------------------------
    add(stage(
        img("av", "assets/avatar.jpg", 532, 528, 193),
        text("c1", 'Web: <u>skojaku.github.io</u>', 700, 358, 32, "", INK, w=1400, align="left"),
        img("bf", "assets/butterfly.png", 738, 520, 80),
        text("c2", "@skojaku.bsky.social", 800, 525, 32, "", INK, w=1400, align="left"),
        text("c3", '<u>skojaku@binghamton.edu</u>', 455, 690, 32, "", INK, w=1700, align="left"),
        img("qr2", "assets/qr.png", 1679, 536, 392)), cls="L-g", header="")
