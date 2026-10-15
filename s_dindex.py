"""Slides 18-34: the disruption index, its failure on the Higgs paper, and why a one-citation change flips it."""
from mm import *  # noqa: F401,F403
import mm

PHOTO = (663, 173, 1199, 533)
CLS = {"hot": HOT, "teal": COOL, "gray": GRAYC}


def edge(name, p, q, ps, qs, color, w=2.2, hs=None, dashed=False):
    x1, y1, x2, y2 = trim(p[0], p[1], q[0], q[1], ps, qs)
    return line(name, x1, y1, x2, y2, color, w, True, dashed, hs)


# ---- citation diagrams: a focal paper (diamond), papers citing it (top), the papers it cites (bottom) ------
DG = {
    # kind: (citing nodes (id, x, y, class), refs (x, y), square size, focal side, edges (src, dst, colour class))
    "dev": ([("p1", -155, -142, "hot"), ("p2", 8, -186, "hot"), ("p3", 161, -138, "hot")],
            [(-167, 154), (-23, 225), (128, 161)], 42, 90,
            [("p1", "F", "hot"), ("p1", "r0", "hot"), ("p2", "F", "hot"), ("p2", "r0", "hot"), ("p3", "F", "hot"),
             ("p3", "r2", "hot")]),
    "dis": ([("g1", -148, -130, "teal"), ("g2", 0, -190, "teal"), ("g3", 158, -121, "teal")],
            [(-134, 136), (-18, 220), (132, 125)], 42, 92,
            [("g1", "F", "teal"), ("g2", "F", "teal"), ("g3", "F", "teal")]),
    "mix": ([("j", -129, -220, "hot"), ("a", -57, -165, "teal"), ("i", 31, -212, "teal"), ("p2", 101, -96, "hot"),
             ("k", -229, -87, "gray"), ("g2", 184, -162, "gray")],
            [(-178, 126), (-49, 206), (120, 141)], 38, 74,
            [("j", "F", "hot"), ("j", "r0", "hot"), ("a", "F", "teal"), ("i", "F", "teal"), ("p2", "F", "hot"),
             ("p2", "r2", "hot"), ("k", "r0", "gray"), ("g2", "r2", "gray")]),
}
MIXLAB = {"j": (-150, -264, HOT), "i": (84, -260, COOL), "k": (-286, -129, GRAYC)}


def diagram(pre, kind, cx, cy, k, labels=False, fade=1.0):
    nodes, refs, ssz, fside, edges = DG[kind]
    pos = {"F": (cx, cy)}
    for nid, x, y, _ in nodes:
        pos[nid] = (cx + k * x, cy + k * y)
    for i, (x, y) in enumerate(refs):
        pos[f"r{i}"] = (cx + k * x, cy + k * y)
    half = ssz * k / 2
    fh = fside * k * 0.5 * 1.414 * 0.72
    cls = {n[0]: n[3] for n in nodes}
    out = []
    w = max(1.7, 2.6 * k)
    hs = 8 + 5 * k
    for ei, (a, b, c) in enumerate(edges):
        out.append(edge(f"{pre}_e{ei}", pos[a], pos[b], half + 2, fh if b == "F" else half + 4, CLS[c], w, hs))
    nr = len(edges)
    for i in range(3):
        out.append(edge(f"{pre}_e{nr + i}", pos["F"], pos[f"r{i}"], fh, half + 4, INK, w * 0.8, hs))
    for nid, x, y, c in nodes:
        out.append(sq(f"{pre}_{nid}", *pos[nid], ssz * k, CLS[c]))
    for i in range(3):
        out.append(sq(f"{pre}_r{i}", *pos[f"r{i}"], ssz * k, PALE))
    out.append(dia(f"{pre}_F", cx, cy, fside * k, DEEP))
    if labels:
        for nm, (x, y, col) in MIXLAB.items():
            out.append(text(f"{pre}_l{nm}", nm, cx + k * x, cy + k * y, 56 * k, "mi", col, w=120))
    return out


# ---- decision trees ----------------------------------------------------------------------------------------
TREE = {
    "concept": dict(
        top=(0, 0, 225, 78), mL=(-132, 171, 225, 78), mR=(201, 176, 222, 78),
        arrows=[(-66, 57, -126, 122), (74, 57, 129, 127), (-181, 223, -241, 297), (-121, 237, -66, 302),
                (177, 237, 177, 310)],
        labels=[("yes", -168, 77), ("no", 174, 95), ("yes", -294, 240), ("no", -26, 259), ("yes", 239, 250)],
        buckets=[(-281, 422), (-66, 422), (184, 412)], bsz=(125, 150), fs=52),
    "higgs": dict(
        top=(0, 0, 185, 66), mL=(-155, 142, 278, 66), mR=(215, 146, 280, 66),
        arrows=[(-53, 49, -103, 102), (65, 49, 109, 102), (-148, 184, -198, 245), (-100, 194, -53, 252),
                (199, 190, 199, 250)],
        labels=[("yes", -138, 64), ("no", 145, 80), ("yes", -243, 200), ("no", -26, 204), ("yes", 252, 212)],
        buckets=[(-230, 337), (-28, 342), (194, 327)], bsz=(125, 150), fs=46),
}
TINT = [("#F3DDD8", HOT), ("#DDE3F2", COOL), ("#E6E6E6", GRAYC)]


def bucket(name, cx, cy, w, h, tint):
    body = (f'<path d="M6,8 L{w - 6},2 L{w - 14},{h - 6} L16,{h} Z" fill="{tint}" stroke="#666666" '
            f'stroke-width="3" stroke-linejoin="round"/>')
    return svg(name, cx - w / 2, cy - h / 2, w, h, body)


def tree(pre, ox, oy, k, mode, boxes, squares, captions=False, labels=True):
    """boxes = (top, left, right) inner html; squares = list of (name, bucket index, dx, dy, fill, ring) in local units."""
    g = TREE[mode]
    P = lambda x, y: (ox + k * x, oy + k * y)
    out = []
    fs = g["fs"] * k * S
    for key, html in zip(("top", "mL", "mR"), boxes):
        x, y, w, h = g[key]
        cx, cy = P(x, y)
        out.append(at(f"{pre}_{key}", cx, cy, w * k, h * k, html, "tb", f"font-size:{fs:.1f}px;"))
    for i, (x1, y1, x2, y2) in enumerate(g["arrows"], 1):
        a, b = P(x1, y1), P(x2, y2)
        out.append(line(f"{pre}_a{i}", a[0], a[1], b[0], b[1], LAV, max(1.6, 2.4 * k), True, False, 8 + 4 * k))
    for i, (t, x, y) in enumerate(g["labels"] if labels else [], 1):
        cx, cy = P(x, y)
        out.append(text(f"{pre}_l{i}", t, cx, cy, 30 * k, "", LAV, w=140))
    bw, bh = g["bsz"]
    for i, (bx, by) in enumerate(g["buckets"]):
        cx, cy = P(bx, by)
        out.append(bucket(f"{pre}_b{i}", cx, cy, bw * k, bh * k, TINT[i][0]))
    for nm, bi, dx, dy, fill, ring in squares:
        bx, by = g["buckets"][bi]
        cx, cy = P(bx + dx, by + dy)
        out.append(sq(f"{pre}_{nm}", cx, cy, (50 if mode == "concept" else 40) * k, fill, ring, 2))
    if captions:
        for i, (t, (dx, dy)) in enumerate(zip(["citing focal<br>& its refs", "citing<br>the focal", "citing its<br>refs only"],
                                              [(-451, 587), (-54, 577), (284, 597)])):
            cx, cy = P(dx, dy)
            out.append(text(f"{pre}_c{i}", t, cx, cy, 30 * k, "", TINT[i][1], w=380, h=170))
    return out


ICD = '<span class="ic dm"></span>'
ICS = '<span class="ic"></span>'
ICE = '<span class="ic eg"></span>'
CITE_TOP = f"cite {ICD}"
CITE_REF = f"cite {ICS}"
CITE_BOTH = f'cite {ICS}<span class="amp">&amp;</span>{ICE}'

SQ_CONCEPT = [("s0", 0, 5, -50, HOT, None), ("s1", 0, -5, 23, HOT, None), ("s2", 1, -3, -35, TEAL, None),
              ("s3", 1, 20, 40, TEAL, None), ("s4", 2, 0, 3, GRAYC, None)]
SQF = "#FFFFFF"
SQ_BEFORE = [("a", 0, 14, -53, SQF, DEEP), ("b", 0, -28, 0, SQF, DEEP), ("c", 0, 7, 45, SQF, DEEP),
             ("d", 1, 0, -23, SQF, DEEP), ("e", 2, 3, -17, SQF, DEEP)]
SQ_AFTER = [("a", 1, -30, -55, SQF, DEEP), ("b", 1, 0, 25, SQF, DEEP), ("c", 1, 30, 45, SQF, DEEP),
            ("d", 1, 0, -22, SQF, DEEP), ("e", 2, 3, -17, SQF, DEEP)]


def higgs_net(red=True):
    """Four papers cite both diamonds; the Higgs paper (blue) cites the Englert-Brout paper (dark)."""
    tops = [(462, 330), (603, 328), (745, 326), (904, 326)]
    H_, E_ = (534, 588), (822, 590)
    refs = [(506, 860), (660, 797), (850, 863)]
    o = []
    for i, t in enumerate(tops):
        o.append(edge(f"hn_t{i}H", t, H_, 40, 52, LAV, 2.4, 11))
        o.append(edge(f"hn_t{i}E", t, E_, 40, 52, LAV, 2.4, 11))
    for i, (src, dst) in enumerate([(H_, refs[0]), (H_, refs[1]), (E_, refs[1]), (E_, refs[2])]):
        o.append(edge(f"hn_r{i}", src, dst, 52, 40, LAV, 2.4, 11))
    for i, t in enumerate(tops):
        o.append(sq(f"hn_s{i}", *t, 75, SQF, DEEP, 2))
    for i, r in enumerate(refs):
        o.append(sq(f"hn_r{i}q", *r, 72, FAINT))
    o.append(dia("hn_H", *H_, 68, DEEP))
    o.append(dia("hn_E", *E_, 68, GRAYC))
    if red:
        o.append(line("hn_red", 590, 592, 765, 592, HOT, 7, True, False, 22))
    return o


BASE_TOPS = [(462, 330), (603, 328), (745, 326), (904, 326)]
BASE_H, BASE_E = (534, 588), (822, 590)
BASE_REFS = [(506, 860), (660, 797), (850, 863)]


def hnet(cx, cy, k, red=True, ghost=False, pre="hn", dims=None):
    """The Higgs / Englert-Brout citation network, drawn at scale k around (cx, cy)."""
    Pt = lambda p: (cx + (p[0] - 680) * k, cy + (p[1] - 590) * k)
    tops = [Pt(p) for p in BASE_TOPS]
    H_, E_ = Pt(BASE_H), Pt(BASE_E)
    refs = [Pt(p) for p in BASE_REFS]
    w, hs, sqs, ds = max(2.0, 2.6 * k), 8 + 4 * k, 75 * k, 68 * k
    o = []
    for i, t in enumerate(tops):
        o.append(edge(f"{pre}_t{i}H", t, H_, sqs * .55, ds * .8, MUTED, w, hs))
        o.append(edge(f"{pre}_t{i}E", t, E_, sqs * .55, ds * .8, MUTED, w, hs))
    for i, (src, dst) in enumerate([(H_, refs[0]), (H_, refs[1]), (E_, refs[1]), (E_, refs[2])]):
        o.append(edge(f"{pre}_r{i}", src, dst, ds * .8, sqs * .55, MUTED, w, hs))
    for i, t in enumerate(tops):
        o.append(sq(f"{pre}_s{i}", *t, sqs, "#FFFFFF", DEEP, 2))
    for i, r in enumerate(refs):
        o.append(sq(f"{pre}_r{i}q", *r, sqs * .96, FAINT))
    o.append(dia(f"{pre}_H", *H_, ds, DEEP))
    o.append(dia(f"{pre}_E", *E_, ds, GRAYC))
    x1, y1, x2, y2 = trim(*H_, *E_, ds * .85, ds * .85)
    if red:
        o.append(line(f"{pre}_red", x1, y1, x2, y2, HOT, 7 * k ** .5, True, False, 22 * k ** .5))
    if ghost:
        o.append(line(f"{pre}_ghost", x1, y1, x2, y2, MUTED, 5 * k ** .5, True, True, 18 * k ** .5))
        o.append(text(f"{pre}_x", "×", (x1 + x2) / 2, y1 - 52 * k, 80 * k ** .5, "", HOT, weight=700, w=200))
    return o, H_, E_


def hlabels(H_, E_, k, pre="hl"):
    return [text(f"{pre}1", "Higgs<br>(1964)", H_[0] - 55 * k - 95, H_[1], 36, "", INK, weight=700, w=190, h=130, align="center"),
            text(f"{pre}2", "Englert &amp; Brout<br>(1964)", E_[0] + 60 * k, E_[1], 36, "", GRAYC, weight=700, w=500, h=130, align="left")]


CAP = ["focal<br>+ refs", "focal<br>only", "refs<br>only"]


def htree(ox, oy, k, boxes, squares, prefix="t"):
    t = tree(prefix, ox, oy, k, "higgs", boxes, squares)
    for i, (bx, by) in enumerate(TREE["higgs"]["buckets"]):
        t.append(text(f"{prefix}_c{i}", CAP[i], ox + k * bx, oy + k * (by + 135), 36, "", TINT[i][1], w=380, h=140))
    return t


SQ4 = lambda b, pos: [(f"s{i}", b, dx, dy, "#FFFFFF", DEEP) for i, (dx, dy) in enumerate(pos)]
POS_HOT = [(-27, -42), (27, -36), (-25, 14), (26, 22)]
POS_COOL = [(-27, -46), (27, -40), (-25, 10), (26, 18)]


def build(add):
    # ---- 18  based on citation networks (the source in grey) ----------------------------------------------------------------------
    add(h2('Based on citation networks <span class="gpar">(Funk &amp; Owen-Smith 2017)</span>') + stage(
        *diagram("dev", "dev", 600, 600, 1.4), *diagram("dis", "dis", 1400, 610, 1.4),
        text("tdev", "developing", 600, 262, 40, "", MUTED, w=600), text("tdis", "disruptive", 1400, 272, 40, "", MUTED, w=600),
        text("dv1", "D=−1", 600, 1000, 52, weight=700, w=400), text("dv2", "D=1", 1400, 1000, 52, weight=700, w=400)),
        cls="L-b")

    # ---- 19  the two ends of a scale, and a mixed case between them ------------------------------------------------------------------
    add(stage(
        *diagram("dev", "dev", 275, 465, 0.74), *diagram("dis", "dis", 1778, 470, 0.74),
        *diagram("mix", "mix", 1078, 881, 0.77, labels=True),
        text("tdev", "developing", 295, 218, 36, "", MUTED, w=600), text("tdis", "disruptive", 1782, 213, 36, "", MUTED, w=600),
        text("dv1", "D=−1", 245, 700, 44, weight=700, w=400), text("dv2", "D=1", 1782, 695, 44, weight=700, w=400),
        line("see_l", 1020, 481, 470, 481, LAV, 5, True, False, 22),
        line("see_r", 1020, 483, 1585, 483, LAV, 5, True, False, 22),
        tri("fulcrum", 1057, 523, 64, 70, DEEP)), cls="L-g")

    # ---- 20  the mixed case is read by a decision tree -------------------------------------------------------------------------------
    add(stage(
        *diagram("mix", "mix", 472, 594, 1.0, labels=True),
        *tree("t", 1466, 243, 1.0, "concept", (CITE_TOP, CITE_REF, CITE_REF), SQ_CONCEPT, captions=True)),
        cls="L-g")

    # ---- 21  ... and counted: the figure stays at full strength, small, on the left; the formula comes next to it ----------------
    fm = ("$$D_{\\blacklozenge}=\\frac{\\textcolor{#3959A6}{n_i}-\\textcolor{#B14434}{n_j}}"
          "{\\textcolor{#3959A6}{n_i}+\\textcolor{#B14434}{n_j}+\\textcolor{#4d4d4d}{n_k}}$$")
    CX = 1110
    add(stage(
        *diagram("mix", "mix", 250, 660, 0.75, labels=True),
        *tree("t", 800, 450, 0.75, "concept", (CITE_TOP, CITE_REF, CITE_REF), SQ_CONCEPT, labels=False),
        box("fcard", CX, 330, 850, 570, "", "", "background:#F7F4F1;"),
        mathbox("fml", CX, 350, 850, 300, fm, 56),
        line("fu1", CX + 262, 672, CX + 342, 672, COOL, 3, False), line("fu2", CX + 482, 672, CX + 562, 672, HOT, 3, False),
        line("fu3", CX + 690, 672, CX + 770, 672, GRAYC, 3, False),
        sq("fk1", CX + 302, 730, 40, COOL), sq("fk2", CX + 522, 730, 40, HOT), sq("fk3", CX + 730, 730, 40, GRAYC),
        text("fx1", "focal<br>only", CX + 302, 845, 36, "", MUTED, w=230, h=130),
        text("fx2", "focal<br>+ refs", CX + 522, 845, 36, "", MUTED, w=230, h=130),
        text("fx3", "refs<br>only", CX + 730, 845, 36, "", MUTED, w=230, h=130)),
        cls="L-g")

    # ---- 22-24  trends found with the D-index: one paper per cut, the earlier ones greyed behind --------------------------------------
    PAP = [("p_team", "assets/paper_team_c.png", "Team size", "Large teams develop, small teams disrupt"),
           ("p_trend", "assets/paper_trend_c.png", "Temporal trend", "Papers are becoming less disruptive over time"),
           ("p_remote", "assets/paper_remote_c.png", "Modes of communication", "Remote collaboration: fewer breakthrough ideas")]
    WP, XS, YP = 1240, (640, 1000, 1360), 540
    GREY = "opacity:.38;filter:grayscale(1);"
    refl = ('<div class="ref">Wu, Wang &amp; Evans (2019) <em>Nature</em> 566. Park, Leahy &amp; Funk (2023) <em>Nature</em> 613. '
            'Lin, Frey &amp; Wu (2023) <em>Nature</em> 623.</div>')

    def papers(upto, ys=YP, w=WP, summary=True, front_grey=False):
        o = []
        for i in range(upto):
            nm, src, cap, summ = PAP[i]
            h = w / mm.aspect(src)
            st = GREY if (i < upto - 1 or front_grey) else ""
            o.append(img(nm, src, XS[i], ys, w, h, "ph", st))
        if summary and upto:
            o.append(text("psum", PAP[upto - 1][3], 1000, 1040, 44, "", "#8a8a8a", w=1900))
        return o

    for k in (1, 2, 3):
        add(stage(*papers(k)) + refl, cls="L-g")

    # ---- 25  ... but the D-index fails ------------------------------------------------------------------------------------------------------
    add(h2('But the D-index <span class="hot">fails</span>', style="font-size:68px;") + '\n\n<p class="sub big">for some well-known disruptive discoveries</p>'
        + stage(*[x for i in range(3) for x in [img(PAP[i][0], PAP[i][1], XS[i] + (i - 1) * 40, 760, 900, 900 / mm.aspect(PAP[i][1]), "ph", GREY)]]) + refl,
        cls="L-b")

    # ---- 26-28  Englert, Brout and Higgs: the photograph in the middle, the story around it -------------------------------------
    PX, PY, PW = 1000, 570, 900                 # photo centre and width (O units); its box in px: x 400..880, y 213..553
    px0, px1 = (PX - PW / 2) * S, (PX + PW / 2) * S
    ph_h = PW / mm.aspect("assets/higgs.jpg")
    py0, py1 = (PY - ph_h / 2) * S, (PY + ph_h / 2) * S
    base = lambda: [
        img("hphoto", "assets/higgs.jpg", PX, PY, PW, None, "ph"),
        text("disc1", "Discovery", 1000, 100, 46, weight=700, w=1500),
        text("disc2", "1964: Englert, Brout and Higgs predict the boson", 1000, 190, 38, w=1900),
        text("rec1", "Recognition", 1000, 940, 46, weight=700, w=1500),
        text("rec2", "2013: Nobel Prize in Physics", 1000, 1030, 38, w=1500)]
    ann1 = lambda: [
        text("an1", "Englert, F.,<br>&amp; Brout, R.<br>(1964)", 270, 480, 36, w=520, h=180),
        text("an1v", "D = 0.15<br>Top 2.8 %", 270, 700, 46, color=HOT, weight=700, w=520, h=150),
        overlay_svg("an1ar", [arrow_px(px0 - 150, 345, px0 + 60, 360, HOT, 5, 20)])]
    ann2 = lambda: [
        text("an2", "Higgs, P.W.<br>(1964)", 1735, 480, 36, w=520, h=150),
        text("an2v", "D = − 0.27<br>Bottom 0.1 %", 1735, 700, 46, color=COOL, weight=700, w=560, h=150),
        text("an2e", "🫠", 1735, 860, 64, w=200),
        overlay_svg("an2ar", [arrow_px(px1 + 150, 345, px1 - 70, 380, COOL, 5, 20)])]
    add(stage(*base()), cls="L-g")
    add(stage(*base(), *ann1()), cls="L-g")
    add(stage(*base(), *ann1(), *ann2()), cls="L-g")

    # ---- 29  what's happening? ----------------------------------------------------------------------------------------------------------
    add(h2('<span class="muted">What’s happening?</span>') + stage(img("hphoto", "assets/higgs.jpg", 1029, 710, 977, None, "ph")),
        cls="L-b")

    # ---- 30-34  why the D-index fails, one change at a time ----------------------------------------------------------------------------
    thumb = lambda: img("hphoto", "assets/higgs.jpg", 1831, 127, 307, None, "ph")
    h2t = h2('<span class="muted">What’s happening?</span>')
    Dlab = lambda cls="", st="": text("hd1", "D = − 0.27<br>Bottom 0.1 %", 480, 800, 44, "", COOL, weight=700, w=640, h=140, align="right", style=st)

    # 30  Higgs cites Englert & Brout
    net_a, Ha, Ea = hnet(760, 625, 1.35)
    add(h2t + stage(thumb(), *net_a, *hlabels(Ha, Ea, 1.35), Dlab(),
                    text("as1", "Higgs cites<br>Englert &amp; Brout.", 1490, 840, 40, "aside", w=700, h=170),
                    overlay_svg("as1ar", [curved_arrow(1250 * S, 810 * S, (Ha[0] + Ea[0]) / 2 * S + 40, (Ha[1] + Ea[1]) / 2 * S + 26, -0.25, MUTED, 3, 16)])),
        cls="L-b")

    # 31  step 1: only that citation is removed
    net_b, Hb, Eb = hnet(760, 625, 1.35, red=False, ghost=True)
    add(h2t + stage(thumb(), *net_b, *hlabels(Hb, Eb, 1.35), Dlab(),
                    text("as1", "Remove this one citation.", 1490, 840, 40, "aside", w=900, h=170)),
        cls="L-b")

    # 32  step 2: the network moves aside and the decision tree appears, with the four papers that cite both
    net_c, Hc, Ec = hnet(470, 650, 0.85, red=False, ghost=True)
    OX, OY = 1450, 300
    add(h2t + stage(thumb(), *net_c, *hlabels(Hc, Ec, 0.85), Dlab(st="opacity:0;"),
                    text("as1", "These four papers<br>cite both.", 470, 215, 40, "aside", w=900, h=170),
                    *htree(OX, OY, 1.0, (CITE_TOP, CITE_BOTH, CITE_BOTH), SQ4(0, POS_HOT))), cls="L-b")

    # 33  step 3: only the four papers move to another box
    add(h2t + stage(thumb(), *net_c, *hlabels(Hc, Ec, 0.85), Dlab(st="opacity:0;"),
                    text("as1", "Without the citation,<br>they move.", 470, 215, 40, "aside", w=900, h=170),
                    *htree(OX, OY, 1.0, (CITE_TOP, CITE_BOTH, CITE_BOTH), SQ4(1, POS_COOL))), cls="L-b")

    # 34  step 4: the result
    add(h2t + stage(thumb(), *net_c, *hlabels(Hc, Ec, 0.85),
                    text("hd1", "D = − 0.27<br>Bottom 0.1 %", 245, 990, 40, "", COOL, weight=700, w=640, h=140, style="opacity:.3;"),
                    overlay_svg("dd_ar", [arrow_px(310, 636, 365, 636, HOT, 5, 16)]),
                    text("hd2", "D = 0.28<br>Top 1.3 %", 800, 990, 52, "", HOT, weight=700, w=640, h=160),
                    *htree(OX, OY, 1.0, (CITE_TOP, CITE_REF, CITE_REF), SQ4(1, POS_COOL))), cls="L-b")

    # ---- 35-37  the same two networks, placed at the height of their D-index ---------------------------------------------------------------
    TT = h2("One citation, a different D-index")
    AX = 330
    yD = lambda D: 560 - D * 520                       # D in [-0.5, 0.5] on this axis
    LY, RY = yD(-0.27), yD(0.28)
    LX, RX = 960, 1560

    def dot_axis(ticks=True, title="D-index", with_left=True, right_val=None, ry=None, dy_right=None):
        o = [line("ax_y", AX, 900, AX, 250, INK, 3.4, True, False, 16),
             text("ax_t", title, AX, 190, 44, "", INK, weight=700, w=700)]
        if ticks:
            for i, (v, lab) in enumerate(((-0.5, "−0.5"), (0, "0"), (0.5, "0.5"))):
                o.append(line(f"tk{i}", AX - 14, yD(v), AX + 14, yD(v), INK, 3, False))
                o.append(text(f"tkl{i}", lab, AX - 90, yD(v), 36, "", MUTED, w=160, align="right"))
        return o

    def lollipop(name, y, x_net, color, label, val_x=None):
        return [line(f"{name}_g", AX + 24, y, x_net - 330, y, color, 3, False, True),
                disc(f"{name}_d", AX, y, 42, color, INK, 3.5),
                text(f"{name}_v", label, AX + 130, y - 56, 44, "", color, weight=700, w=420)]

    nL, HL, EL = hnet(LX, LY, 0.72, pre="ha")
    add(TT + stage(*dot_axis(), *lollipop("pl", LY, LX, COOL, "−0.27"), *nL,
                   text("cl", "Higgs cites Englert &amp; Brout", LX, LY + 215, 36, "", MUTED, w=900)), cls="L-b")

    nR, HR, ER = hnet(RX, RY, 0.72, red=False, ghost=True, pre="hb")
    jump = [overlay_svg("jmp", [arrow_px(AX * S + 70, LY * S - 30, AX * S + 70, RY * S + 40, HOT, 5, 18)]),
            text("jt", "0.55", AX + 330, (LY + RY) / 2, 52, "", HOT, weight=700, w=300)]
    add(TT + stage(*dot_axis(), *lollipop("pl", LY, LX, COOL, "−0.27"), *nL,
                   text("cl", "Higgs cites Englert &amp; Brout", LX, LY + 215, 36, "", MUTED, w=900),
                   *lollipop("pr", RY, RX, HOT, "0.28"), *nR,
                   text("cr", "one citation removed", RX, RY + 250, 36, "", MUTED, w=900), *jump), cls="L-b")

    # the same two networks under a continuous measure (a sketch, no numbers)
    RY2 = yD(-0.31)
    nR2, HR2, ER2 = hnet(RX, RY2, 0.72, red=False, ghost=True, pre="hb")
    add(TT.replace("One citation, a different D-index", "A continuous measure does not jump") + stage(
        *dot_axis(ticks=False, title="EDM (sketch)"), *lollipop("pl", LY, LX, COOL, ""), *nL,
        *lollipop("pr", RY2, RX, HOT, ""), *nR2,
        text("as1", "tiny change,<br>tiny effect", 1100, 330, 44, "aside", w=900, h=170))
        + '\n\n<p class="take">We preserve <span class="hot">continuity</span> by abandoning class rounding.</p>', cls="L-b")
