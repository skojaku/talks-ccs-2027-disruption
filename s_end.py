"""Slides 70-81: the measure, the test, the results, the summary and the contact slide."""
from mm import *  # noqa: F401,F403
import mm
from s_walk import STATES, GRAYP, RING


def stage_free(objs):
    return objs


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
    L = {"t": [(498, 570), (641, 570), (804, 570)], "m": [(463, 716), (716, 716)], "b": [(544, 835), (663, 835)]}
    R = {"t": [(1392, 555), (1536, 556), (1699, 556)], "m": [(1357, 702), (1610, 702)], "b": [(1438, 822), (1558, 822)]}

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
        text("n1", "original network", 663, 490, 36, "", MUTED, weight=700, w=900),
        text("n2", "random network", 1573, 487, 36, "", MUTED, weight=700, w=900),
        line("tm1", 297, 865, 297, 495, LAV, 6, True, False, 28), line("tm2", 1230, 865, 1230, 495, LAV, 6, True, False, 28),
        text("tl1", "Time", 245, 680, 36, "", LAV, weight=700, w=300, style="transform:rotate(-90deg);"),
        text("tl2", "Time", 1178, 680, 36, "", LAV, weight=700, w=300, style="transform:rotate(-90deg);")), cls="L-b")

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
        img("odds", "assets/odds_ratio.png", 1275, 650, 1240, None, ""),
        *lab("o1", "Control<br>variable", 180, 440, 655, 388), *lab("o2", "EDM<br>(proposed)", 290, 650, 672, 625),
        *lab("o3", "D-index", 320, 840, 682, 840),
        img("apsc", "assets/aps_news.png", 255, 1050, 440, None)), cls="L-b")

    # ---- 78-81  summary: "Summary", then the three claims, one more at every cut -------------------------------------------------
    add(h2("Summary"), cls="L-f", header="")
    SUMM = [
        ("k1", 230, lambda: img("sm1", "assets/higgs.jpg", 330, 230, 420, None, "ph"),
         'The D-index <span class="hot">fails</span> on<br>well-known discoveries', "Higgs (1964): D = −0.27, Bottom 0.1 %"),
        ("k2", 585, lambda: stage_free(scatter_thumb(330, 585, 0.24)),
         'EDM keeps <span class="hot">continuity</span>', "A large query-key gap marks a discontinuity"),
        ("k3", 940, lambda: img("sm3", "assets/odds_ratio.png", 330, 940, 420, None, ""),
         'EDM matches <span class="hot">human judgment</span>', "Odds ratio 1.23, against 1.03 for the D-index"),
    ]
    for n in range(1, 4):
        objs = []
        for key, y, pic, head, sub in SUMM[:n]:
            pics = pic()
            objs += pics if isinstance(pics, list) else [pics]
            objs.append(text(key, head, 660, y - 50, 46, "", INK, weight=700, w=1280, h=190, align="left"))
            objs.append(text(key + "s", sub, 660, y + 92, 38, "", MUTED, w=1280, align="left"))
        add(stage(*objs), cls="L-g")

    # ---- 82  the paper (screenshot, one QR code with its DOI) and where to find me ---------------------------------------------------
    add(stage(
        img("paperimg", "assets/sciadv.png", 560, 395, 1000, None, "ph"),
        text("papercap", "<em>Science Advances</em> 12, eadx3420 (2026)", 560, 770, 36, w=1500),
        text("paperlead", "Read the paper", 1560, 170, 52, weight=700, w=800),
        img("qrpaper", "assets/qr_paper.png", 1560, 520, 460),
        text("qrcap", "doi.org/10.1126/<br>sciadv.adx3420", 1560, 830, 36, "", MUTED, w=800, h=150),
        img("av", "assets/avatar.jpg", 160, 925, 150),
        text("c1", 'Web: <u>skojaku.github.io</u>', 300, 880, 36, "", INK, w=1300, align="left"),
        img("bf", "assets/butterfly.png", 334, 955, 56),
        text("c2", "@skojaku.bsky.social", 400, 955, 36, "", INK, w=1300, align="left"),
        text("c3", '<u>skojaku@binghamton.edu</u>', 300, 1030, 36, "", INK, w=1400, align="left")), cls="L-g", header="")
