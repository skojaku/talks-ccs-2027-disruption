"""Slides 21-35: the disruption index, its failure on the Higgs paper, and what rounding does."""
from mm import *  # noqa: F401,F403
import mm

CLS = {"hot": HOT, "teal": TEAL, "gray": GRAYC}


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
MIXLAB = {"j": (-150, -264, HOT), "i": (84, -260, TEAL), "k": (-286, -129, GRAYC)}


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
TINT = [("#FBE3D3", HOT), ("#D9ECEA", TEAL), ("#E6E2DE", GRAYC)]


def bucket(name, cx, cy, w, h, tint):
    body = (f'<path d="M6,8 L{w - 6},2 L{w - 14},{h - 6} L16,{h} Z" fill="{tint}" stroke="#6F6A66" '
            f'stroke-width="3" stroke-linejoin="round"/>')
    return svg(name, cx - w / 2, cy - h / 2, w, h, body)


def tree(pre, ox, oy, k, mode, boxes, squares, captions=False):
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
    for i, (t, x, y) in enumerate(g["labels"], 1):
        cx, cy = P(x, y)
        out.append(text(f"{pre}_l{i}", t, cx, cy, 26 * k, "", LAV, w=140))
    bw, bh = g["bsz"]
    for i, (bx, by) in enumerate(g["buckets"]):
        cx, cy = P(bx, by)
        out.append(bucket(f"{pre}_b{i}", cx, cy, bw * k, bh * k, TINT[i][0]))
    for nm, bi, dx, dy, fill, ring in squares:
        bx, by = g["buckets"][bi]
        cx, cy = P(bx + dx, by + dy)
        out.append(sq(f"{pre}_{nm}", cx, cy, (50 if mode == "concept" else 40) * k, fill, ring, 2))
    if captions:
        for i, (t, (dx, dy)) in enumerate(zip(["citing focal<br>& its refs", "citing<br>the focal", "citing its<br>refs but<br>focal"],
                                              [(-451, 587), (-54, 577), (284, 597)])):
            cx, cy = P(dx, dy)
            out.append(text(f"{pre}_c{i}", t, cx, cy, 24 * k, "", TINT[i][1], w=380, h=170))
    return out


ICD = '<span class="ic dm"></span>'
ICS = '<span class="ic"></span>'
ICE = '<span class="ic eg"></span>'
CITE_TOP = f"cite {ICD}"
CITE_REF = f"cite {ICS}"
CITE_BOTH = f'cite {ICS}<span class="amp">&amp;</span>{ICE}'

SQ_CONCEPT = [("s0", 0, 5, -50, HOT, None), ("s1", 0, -5, 23, HOT, None), ("s2", 1, -3, -35, TEAL, None),
              ("s3", 1, 20, 40, TEAL, None), ("s4", 2, 0, 3, GRAYC, None)]
SQF = "#F6F7FC"
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


def build(add):
    HD = "Disruption index (Funk and Owen-Smith 2017)"

    # ---- 21  based on citation networks ------------------------------------------------------------------------
    add(h2("Based on citation networks") + stage(
        *diagram("dev", "dev", 753, 619, 1), *diagram("dis", "dis", 1346, 635, 1),
        text("tdev", "developing", 745, 353, 30, "", MUTED, w=600), text("tdis", "disruptive", 1345, 363, 30, "", MUTED, w=600),
        text("dv1", "D=−1", 747, 913, 40, weight=700, w=400), text("dv2", "D=1", 1320, 925, 40, weight=700, w=400)),
        cls="L-b", header=HD)

    # ---- 22  the two ends of a scale, and a mixed case between them ----------------------------------------------
    add(stage(
        *diagram("dev", "dev", 275, 465, 0.74), *diagram("dis", "dis", 1778, 470, 0.74),
        *diagram("mix", "mix", 1078, 881, 0.77, labels=True),
        text("tdev", "developing", 295, 218, 30, "", MUTED, w=600), text("tdis", "disruptive", 1782, 213, 30, "", MUTED, w=600),
        text("dv1", "D=−1", 245, 700, 40, weight=700, w=400), text("dv2", "D=1", 1782, 695, 40, weight=700, w=400),
        line("see_l", 1020, 481, 470, 481, LAV, 5, True, False, 22),
        line("see_r", 1020, 483, 1585, 483, LAV, 5, True, False, 22),
        tri("fulcrum", 1057, 523, 64, 70, DEEP)), cls="L-g", header=HD)

    # ---- 23  the mixed case is read by a decision tree ----------------------------------------------------------------
    add(stage(
        *diagram("mix", "mix", 472, 594, 1.0, labels=True),
        *tree("t", 1466, 243, 1.0, "concept", (CITE_TOP, CITE_REF, CITE_REF), SQ_CONCEPT, captions=True)),
        cls="L-g", header=HD)

    # ---- 24  ... and counted ---------------------------------------------------------------------------------------------
    fm = ("$$D_{\\blacklozenge}=\\frac{\\textcolor{#3F8A88}{n_i}-\\textcolor{#D9631E}{n_j}}"
          "{\\textcolor{#3F8A88}{n_i}+\\textcolor{#D9631E}{n_j}+\\textcolor{#5E5A57}{n_k}}$$")
    add(stage(
        *diagram("mix", "mix", 328, 590, 0.84, labels=True),
        *tree("t", 837, 401, 0.72, "concept", (CITE_TOP, CITE_REF, CITE_REF), SQ_CONCEPT),
        box("fcard", 1150, 387, 835, 408, "", "", f"background:#F7F4F1;"),
        mathbox("fml", 1150, 400, 835, 300, fm, 54),
        line("fu1", 1432, 672, 1512, 672, TEAL, 3, False), line("fu2", 1652, 672, 1732, 672, HOT, 3, False),
        line("fu3", 1860, 672, 1940, 672, GRAYC, 3, False),
        sq("fk1", 1472, 722, 40, TEAL), sq("fk2", 1692, 722, 40, HOT), sq("fk3", 1900, 722, 40, GRAYC),
        text("counts", "counts", 1560, 845, 34, "aside", w=400),
        overlay_svg("counts_ar", [curved_arrow(1640 * S, 820 * S, 1695 * S, 775 * S, -0.3, MUTED, 2.4, 14)])),
        cls="L-g", header=HD)

    # ---- 25  trends found with the D-index ----------------------------------------------------------------------------------
    pap = lambda: [img("p_team", "assets/paper_team.png", 372, 372, 540, None, "ph"),
                   img("p_trend", "assets/paper_trend.png", 987, 372, 540, None, "ph"),
                   img("p_remote", "assets/paper_remote.png", 1604, 372, 540, 540 / mm.aspect("assets/paper_remote.png"), "ph"),
                   text("c_team", "Team size", 372, 760, 30, w=700),
                   text("c_trend", "Temporal Trend", 987, 760, 30, w=700),
                   text("c_remote", "Modes of Communication", 1604, 760, 30, w=800)]
    refl = ('<div class="ref">Wu, Wang &amp; Evans (2019) <em>Nature</em> 566. Park, Leahy &amp; Funk (2023) <em>Nature</em> 613. '
            'Lin, Frey &amp; Wu (2023) <em>Nature</em> 623.</div>')
    add(stage(*pap()) + refl, cls="L-g", header="")
    add(stage(*pap()) + refl + '\n\n<p class="take dark" style="padding-right:150px">BUT, the D-index <span class="hot">fails</span> for some well-known '
        'disruptive discoveries</p>', cls="L-g")

    # ---- 27-29  Englert, Brout and Higgs ----------------------------------------------------------------------------------------
    bl = ('<div class="o blist" style="left:50px;top:200px;width:560px">\n\n'
          "- Discovery\n  - 1964: Englert, Brout and Higgs predict the boson\n"
          "- Recognition\n  - 2013: Nobel Prize in Physics\n\n</div>")
    ph = lambda: img("hphoto", "assets/higgs.jpg", 1420, 532, 780, None, "ph")
    ann1 = lambda: [
        text("an1", "Englert, F.,<br>&amp; Brout, R. (1964)", 1088, 108, 32, w=620, h=130),
        text("an1v", f"D = 0.15<br>Top 2.8 %", 1640, 115, 44, color=HOT, weight=700, w=420, h=130),
        overlay_svg("an1ar", [curved_arrow(718, 118, 766, 192, 0.18, HOT, 7, 26)])]
    ann2 = lambda: [
        text("an2", "Higgs, P.W. (1964)", 1437, 885, 32, w=800),
        text("an2v", "D = − 0.27<br>Bottom 0.1 %", 1560, 1020, 44, color=COOL, weight=700, w=520, h=130),
        text("an2e", "🫠", 1815, 950, 58, w=200),
        overlay_svg("an2ar", [curved_arrow(1068, 538, 1038, 448, -0.18, HOT, 7, 26)])]
    add(stage(ph(), bl), cls="L-b")
    add(stage(ph(), bl, *ann1()), cls="L-b")
    add(stage(ph(), bl, *ann1(), *ann2()), cls="L-b")

    # ---- 30  what's happening? ----------------------------------------------------------------------------------------------------
    add(h2('<span class="muted">What’s happening?</span>') + stage(img("hphoto", "assets/higgs.jpg", 1029, 710, 977, None, "ph")),
        cls="L-b")

    # ---- 31-33  the Higgs paper cites the Englert-Brout paper ---------------------------------------------------------------------
    thumb = lambda: img("hphoto", "assets/higgs.jpg", 1831, 127, 307, None, "ph")
    hlab = lambda: [text("hl1", "Higgs, P.W.<br>(1964)", 248, 380, 30, weight=700, w=420, h=130),
                    text("hl2", "Englert, F.,<br>&amp; Brout, R.<br>(1964)", 1020, 610, 30, color=GRAYC, w=420, h=200)]
    dlab = lambda cls="": text("hd1", "D = − 0.27<br>Bottom 0.1 %", 262, 535, 34, "aside " + cls, w=520, h=150)
    T0 = lambda: tree("ht", 1598, 438, 1.0, "higgs", (CITE_TOP, CITE_BOTH, CITE_BOTH), SQ_BEFORE)
    h2t = h2('<span class="muted">What’s happening?</span>')
    add(h2t + stage(thumb(), *higgs_net(True), *hlab(), dlab(), *T0()), cls="L-b")
    add(h2t + stage(thumb(), *higgs_net(False), *hlab(), dlab(), *T0()), cls="L-b")
    T1 = tree("ht", 1598, 438, 1.0, "higgs", (CITE_TOP, CITE_REF, CITE_REF), SQ_AFTER)
    add(h2t + stage(thumb(), *higgs_net(False), *hlab(), dlab("past"),
                    overlay_svg("dd_ar", [f'<path d="M158,423 L158,478" stroke="{HOT}" stroke-width="4" stroke-linecap="round"/>'
                                          f'<path d="M144,466 L158,482 L172,466" fill="none" stroke="{HOT}" stroke-width="4" '
                                          f'stroke-linecap="round" stroke-linejoin="round"/>']),
                    text("hd2", "D = 0.28<br>Top 1.3 %", 262, 880, 54, "aside", HOT, w=640, h=190), *T1), cls="L-b")

    # ---- 34-35  many citations are rounded into another class ----------------------------------------------------------------------
    ttl = h2('Citations are “<em class="hot">rounded</em>” into classes.')
    pair = lambda: [
        *tree("u", 475, 465, 0.78, "higgs", (CITE_TOP, CITE_BOTH, CITE_BOTH), SQ_BEFORE),
        *tree("ht", 1545, 431, 0.78, "higgs", (CITE_TOP, CITE_REF, CITE_REF), SQ_AFTER),
        text("rm", "Removal of a<br>single citation.", 1050, 520, 28, "", MUTED, weight=700, w=500, h=150),
        overlay_svg("rm_ar", [f'<path d="M528,392 L772,392" stroke="{LAV}" stroke-width="5" stroke-linecap="round"/>'
                              f'<path d="M752,376 L774,392 L752,408" fill="none" stroke="{LAV}" stroke-width="4" '
                              f'stroke-linecap="round" stroke-linejoin="round"/>'])]
    add(ttl + stage(*pair()), cls="L-b")
    add(ttl + stage(*pair()) + '\n\n<p class="take">We preserve <span class="hot">continuity</span> by abandoning class rounding.</p>',
        cls="L-b")
