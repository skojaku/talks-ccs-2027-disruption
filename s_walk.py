"""Random walks, the training pairs (ancestor, descendant), and, after word2vec, the embedding space where query and key move."""
from mm import *  # noqa: F401,F403
import mm

GR = "#A6A6A6"          # the grey of an unnamed walk node
RING = "#4d4d4d"
SEQ = [GR, TEAL, OLIVE, HOT, COOL, DEEP]
TREE_POS = [(517, 48), (520, 182), (372, 400), (667, 400), (252, 576), (520, 550), (157, 737), (644, 721),
            (396, 808), (447, 994)]
TREE_COL = [GR, TEAL, OLIVE, GR, GR, HOT, GR, GR, COOL, DEEP]
WALK = [0, 1, 2, 5, 8, 9]                       # the tree nodes the walk visits, in order
SEQ_X = [1030, 1201, 1372, 1543, 1715, 1887]
PAIRS = [(HOT, DEEP), (HOT, COOL), (OLIVE, COOL), (OLIVE, HOT), (TEAL, HOT), (TEAL, OLIVE), (GR, OLIVE), (GR, TEAL)]


def walk_tree(dx=0):
    """The tree of walks (left of the slide). `seq` = list of names for discs lying on the walk's nodes."""
    o = []
    TP = [(x + dx, y) for x, y in TREE_POS]
    E = [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (4, 6), (4, 8), (5, 8), (5, 7)]
    for i, (a, b) in enumerate(E):
        o.append(edge_(f"w_e{i}", TP[a], TP[b], 40, 44, "#333333", 3.2))
    o.append(edge_("w_e9", TP[8], TP[9], 40, 44, "#9a9a9a", 3.2))
    for i, (src, dst) in enumerate([(6, (60, 945)), (6, (240, 945)), (8, (325, 950)), (8, (512, 945)), (7, (648, 955))]):
        o.append(edge_(f"w_d{i}", TP[src], (dst[0] + dx, dst[1]), 40, 0, "#9a9a9a", 3, dashed=True))
    for i, (p, c) in enumerate(zip(TP, TREE_COL)):
        o.append(disc(f"w_n{i}", *p, 78, c, RING, 3.5))
    return o


def edge_(name, p, q, ps, qs, color, w=3.0, dashed=False):
    x1, y1, x2, y2 = trim(p[0], p[1], q[0], q[1], ps, qs)
    return line(name, x1, y1, x2, y2, color, w, True, dashed, 13)


def pair(name, i, cx, cy, d, op=1.0):
    ca, cb = PAIRS[i]
    ds = d * S
    inner = "".join(f'<span class="pd" style="width:{ds:.1f}px;height:{ds:.1f}px;background:{c}"></span>' for c in (ca, cb))
    return at(name, cx, cy, d * 2.6, d * 1.1, inner, "pair", f"gap:{d * 0.28 * S:.1f}px;" + (f"opacity:{op};" if op != 1 else ""))


SMALL_Y = {7: 987, 6: 912, 5: 838, 4: 758, 3: 688, 2: 610}
BIG_Y = [250 + 105 * i for i in range(8)]
WIN_C = [SEQ_X[w] for w in range(4)]


ARC_L = ("parent → child", 450)                  # the label of each arc and its width (O units), set at the type floor
ARC_LL = ("grandparent → grandchild", 790)


def clamp(cx, w, lo=40, hi=1960):
    """Keep a label of width w centred near cx but inside the slide."""
    return min(max(cx, lo + w / 2), hi - w / 2)


def walk_state(w, cur_pairs=True, list_upto=None):
    """Slides with the window at position w: the sequence, the window, the arcs (parent -> child above the row,
    grandparent -> grandchild below it), the pairs so far."""
    o = []
    for k, x in enumerate(SEQ_X):
        o.append(disc(f"s{k}", x, 295, 80, SEQ[k], RING, 3.5))
    left, right = SEQ_X[w] - 78, SEQ_X[w + 2] + 66
    o.append(box("win", left, 242, right - left, 110, "", "", f"border:4px solid {HOT};"))
    c0, c1, c2 = SEQ_X[w], SEQ_X[w + 1], SEQ_X[w + 2]
    o.append(overlay_svg("arcs", [curved_arrow(c0 * S, 238 * S, (c1 - 22) * S, 212 * S, -0.6, MUTED, 4, 18),
                                   curved_arrow(c0 * S, 358 * S, (c2 - 8) * S, 360 * S, 0.45, MUTED, 4, 18)]))
    o.append(text("arcl1", ARC_L[0], clamp((c0 + c1) / 2, ARC_L[1]), 122, 36, "", MUTED, w=ARC_L[1]))
    o.append(text("arcl2", ARC_LL[0], clamp((c0 + c2) / 2, ARC_LL[1]), 492, 36, "", MUTED, w=ARC_LL[1]))
    cx = (left + right) / 2 + 30
    o.append(text("qk", "(ancestor, descendant)", clamp(cx, 640), 625 + 3 * w, 36, "", INK, w=640))
    if w == 0:
        o.append(text("tdlab", "Training data", cx, 975, 30, "", "#9a9a9a", weight=700, w=700))
    else:
        o.append(text("tdlab", "Training data", 800, 740, 30, "", "#9a9a9a", weight=700, w=700,
                      style="transform:rotate(-90deg);"))
    upto = w if list_upto is None else list_upto
    for wi in range(upto):
        for L in (6 - 2 * wi, 7 - 2 * wi):
            o.append(pair(f"pr{L}", L, 921, SMALL_Y[L], 62))
    if cur_pairs:
        for r, L in enumerate((6 - 2 * w, 7 - 2 * w)):
            y = (735 + 16 * w) if r == 0 else (854 + 21 * w)
            o.append(pair(f"pr{L}", L, cx, y, 75))
    return o


def big_list(focus=None, head="(ancestor, descendant)"):
    """All the pairs. Before word2vec they are (ancestor, descendant); after it, the same pairs are (query, key)."""
    o = [text("lh", head, 1037, 135, 34, "", INK, w=800)]
    if not focus:
        o.append(text("tdlab", "Training data", 815, 580, 30, "", "#9a9a9a", weight=700, w=700, style="transform:rotate(-90deg);"))
    for L in range(8):
        o.append(pair(f"pr{L}", L, 1038, BIG_Y[L], 96, 0.3 if focus and L not in focus else 1.0))
    return o


# ---- the embedding space ---------------------------------------------------------------------------------------------
GRAYP = "#E0E0E0"
STATES = {
    "small": dict(ax=((675, 565), (675, 832), (880, 832)), d=50,
                  gray=[(977, 293), (1625, 340), (1692, 445), (1530, 460), (1411, 567), (1536, 687)],
                  teal=(916, 398), olive=(973, 530), fq=(1282, 450), fk=(1282, 450), lb=(1544, 285), db=(1703, 597)),
    "big": dict(ax=((120, 610), (120, 1085), (485, 1085)), d=80,
                gray=[(430, 362), (1563, 443), (1681, 628), (1397, 654), (1191, 841), (1410, 1050)],
                teal=(324, 548), olive=(423, 778), fq=(963, 637), fk=(963, 637), lb=(1423, 350), db=(1701, 890)),
    "split": dict(ax=((120, 610), (120, 1085), (485, 1085)), d=80,
                  gray=[(430, 362), (1563, 443), (1681, 628), (1397, 654), (1191, 841), (1410, 1050)],
                  teal=(434, 570), olive=(523, 725), fq=(1128, 686), fk=(826, 639), lb=(1360, 412), db=(1601, 857)),
    "nm": dict(ax=None, d=56,
               gray=[(98, 287), (868, 340), (922, 469), (756, 483), (638, 610), (764, 752)],
               teal=(100, 428), olive=(160, 532), fq=(572, 505), fk=(368, 472), lb=(730, 320), db=(893, 622)),
}


def scatter(state, key_visible=False, faded=False):
    st = STATES[state]
    d = st["d"]
    o = []
    if st["ax"]:
        (x0, y0), (x1, y1), (x2, y2) = st["ax"]
        o += [line("ax_y", x1, y1, x0, y0, "#B3B3B3", 3.4, True, False, 16), line("ax_x", x1 - 2, y1, x2, y2, "#B3B3B3", 3.4, True, False, 16)]
    for i, p in enumerate(st["gray"]):
        o.append(disc(f"sg{i}", *p, d, FAINT, GRAYP, 3))
    fo = 0.55 if state in ("split", "nm") else 1.0
    o.append(disc("st", *st["teal"], d, TEAL, RING, 3.5, opacity=fo))
    o.append(disc("so", *st["olive"], d, OLIVE, RING, 3.5, opacity=fo))
    o.append(disc("sk", *st["fk"], d, HOT, RING, 3.5, dashed=True, opacity=1.0 if key_visible else 0.0))
    o.append(disc("sq", *st["fq"], d, HOT, INK, 3.5))
    o.append(disc("sb", *st["lb"], d, COOL, RING, 3.5, dashed=True, opacity=fo))
    o.append(disc("sd", *st["db"], d, DEEP, RING, 3.5, dashed=True, opacity=fo))
    return o


def aro(name, p, q, color, dashed=False, w=5):
    return line(name, p[0], p[1], q[0], q[1], color, w, True, dashed, 22 if w >= 5 else 15)


DX = 630                                             # the tree sits mid-slide until the sequence needs the room
PTS = [(470, 55), (465, 150), (380, 260), (285, 330), (300, 440), (420, 540), (430, 640), (350, 760), (310, 850), (345, 965)]


def brush(dx=0):
    return overlay_svg("wbrush", [brush_path([((x + dx) * S, y * S) for x, y in PTS], GOLD, 14, 0.95)
                                  + f'<path class="ahead" d="M{(262 + dx) * S:.1f},{925 * S:.1f} L{(345 + dx) * S:.1f},{972 * S:.1f} L{(358 + dx) * S:.1f},{880 * S:.1f}" fill="none" '
                                    f'stroke="{GOLD}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'])


rwt = lambda dx=0, col=INK: text("rw", "Random<br>walks", 215 + dx, 230, 52, "", col, w=520, h=200, style="transform:rotate(-34deg);")
onwalk = lambda dx=0: [disc(f"s{k}", TREE_POS[WALK[k]][0] + dx, TREE_POS[WALK[k]][1], 80, SEQ[k], RING, 3.5) for k in range(6)]


def build_a1(add):
    # ---- the tree of random walks, the walk, and the sequence it gives ------------------------------------------------------------
    add(stage(*walk_tree(DX), text("rwtitle", "Simulate the flow<br>of knowledge<br>with random walks", 40, 480, 44, "", INK, weight=700, w=900, h=330, align="left")), cls="L-g", header="")
    add(stage(*walk_tree(DX), brush(DX), rwt(DX), *onwalk(DX)), cls="L-g")
    seq0 = [disc(f"s{k}", SEQ_X[k], 295, 80, SEQ[k], RING, 3.5) for k in range(6)]
    add(stage(*walk_tree(), brush(), rwt(), *seq0), cls="L-g")


def build_a2(add):
    # ---- the window slides along the sequence and collects pairs (the tree is muted once the sequence has left it) ----------------
    TREE_ONLY = lambda: [*walk_tree(), brush(), rwt(0, MUTED)]
    add(stage(*TREE_ONLY(), *walk_state(0)), cls="L-g")
    add(stage(*TREE_ONLY(), *walk_state(1)), cls="L-g")
    add(stage(*TREE_ONLY(), *walk_state(2, cur_pairs=False)), cls="L-g")
    add(stage(*TREE_ONLY(), *walk_state(2)), cls="L-g")
    add(stage(*TREE_ONLY(), *walk_state(3)), cls="L-g")
    # ---- all the pairs -----------------------------------------------------------------------------------------------------------
    add(stage(*big_list()), cls="L-g")


def focus(add):
    # ---- after word2vec: the same pairs, now (query, key); focus on one paper (morphs into the embedding space) --------------
    FOC = {0, 1, 3, 4}
    add(stage(*big_list(FOC, "(query, key)"),
              text("as1", "Let’s focus on<br>this paper.", 470, 540, 38, "aside", w=720, h=170,
                   style="transform:rotate(-14deg);"),
              overlay_svg("as1ar", [curved_arrow(420, 290, 590, 195, 0.3, MUTED, 3, 16)]),
              text("as2", "irrelevant to the<br>focal paper", 1560, 800, 38, "aside", w=720, h=170,
                   style="transform:rotate(-8deg);"),
              overlay_svg("as2ar", [curved_arrow(885, 575, 748, 622, -0.3, MUTED, 3, 16)])), cls="L-g")


def build_b(add):
    FOC = None
    # ---- 64-65  the embedding space ----------------------------------------------------------------------------------------
    def small_list():
        o = [text("lh", "(query, key)", 466, 248, 28, "", INK, w=700)]
        for L, y in ((0, 348), (1, 453), (3, 575), (4, 675)):
            o.append(pair(f"pr{L}", L, 466, y, 82))
        o.append(text("as1", "Let’s focus on<br>this paper.", 175, 625, 34, "aside", w=720, h=170,
                      style="transform:rotate(-38deg);"))
        o.append(overlay_svg("as1ar", [curved_arrow(133, 345, 223, 262, -0.1, MUTED, 3, 16)]))
        return o

    fp = lambda: text("fp", "focal<br>paper", 1283, 305, 44, "", HOT, w=560, h=200)
    take = text("tk", "Paired query &amp; key<br>get closer.", 1490, 950, 44, "", INK, weight=700, w=900, h=170)
    add(stage(*small_list(), *scatter("small"), fp(), take), cls="L-g")
    arrows_small = [aro("ar1", (940, 404), (1018, 420), TEAL), aro("ar2", (997, 530), (1070, 497), OLIVE),
                    aro("ar3", (1300, 445), (1375, 392), HOT), aro("ar4", (1300, 455), (1405, 487), HOT),
                    aro("ar5", (1258, 447), (1150, 427), HOT, True), aro("ar6", (1258, 457), (1148, 492), HOT, True),
                    aro("ar7", (1523, 298), (1452, 342), COOL, True), aro("ar8", (1680, 590), (1580, 550), DEEP, True)]
    add(stage(*small_list(), *scatter("small"), fp(), take, *arrows_small), cls="L-g")

    # ---- 66  zoom in ---------------------------------------------------------------------------------------------------------------
    fp2 = lambda: text("fp", "focal<br>paper", 948, 225, 44, "", HOT, w=560, h=200)
    arrows_big = [aro("ar1", (365, 553), (505, 585), TEAL), aro("ar2", (472, 771), (595, 720), OLIVE),
                  aro("ar3", (995, 610), (1130, 533), HOT), aro("ar4", (1005, 645), (1180, 700), HOT),
                  aro("ar5", (925, 625), (728, 605), HOT, True), aro("ar6", (925, 660), (730, 730), HOT, True),
                  aro("ar7", (1385, 368), (1258, 447), COOL, True), aro("ar8", (1665, 872), (1485, 812), DEEP, True)]
    add(stage(*scatter("big"), fp2(), *arrows_big), cls="L-g")

    # ---- 67  query and key of one paper pull apart ---------------------------------------------------------------------------
    box_ = lambda n, x0, y0, x1, y1, t: [box(n, x0, y0, x1 - x0, y1 - y0, "", "", "background:#F9F5DA;"),
                                         text(n + "t", t, (x0 + x1) / 2, (y0 + y1) / 2, 40, "", HOT, w=x1 - x0, h=y1 - y0)]
    add(stage(*scatter("split", key_visible=True), fp2(),
              text("kl", "k<sub>i</sub>", 740, 575, 52, "mi", INK, w=200), text("ql", "q<sub>i</sub>", 1133, 600, 52, "mi", INK, w=200),
              *box_("kb", 618, 723, 903, 929, "key<br>vec"), *box_("qb", 1043, 740, 1298, 945, "query<br>vec")), cls="L-g")

    # ---- 68  not mixed / mixed ----------------------------------------------------------------------------------------------------
    nm_extra = [text("ti1", "Not mixed", 490, 105, 36, "", MUTED, weight=700, w=700),
                text("ti2", "Mixed", 1597, 105, 36, "", MUTED, weight=700, w=700),
                aro("na1", (125, 436), (220, 440), TEAL, w=4), aro("na2", (185, 530), (255, 522), OLIVE, w=4),
                aro("na3", (345, 465), (258, 452), HOT, True, 4), aro("na4", (340, 492), (285, 514), HOT, True, 4),
                aro("na5", (600, 490), (657, 442), HOT, w=4), aro("na6", (600, 522), (680, 555), HOT, w=4),
                aro("na7", (718, 347), (693, 393), COOL, True, 4), aro("na8", (872, 610), (820, 592), DEEP, True, 4),
                text("nkl", "k<sub>i</sub>", 338, 405, 40, "mi", INK, w=200), text("nql", "q<sub>i</sub>", 580, 432, 40, "mi", INK, w=200),
                text("nfp", "focal<br>paper", 463, 275, 36, "", HOT, w=560, h=200, style="opacity:.45;"),
                line("div", 1100, 220, 1100, 725, MUTED, 3, False, True),
                text("cap1", "Large separation<br>of<br>key and query", 545, 945, 34, "", INK, w=1000, h=260),
                text("tilde", "∼", 975, 912, 60, "", INK, w=200),
                text("cap2", "Discontinuity of citing<br>and cited papers", 1520, 930, 34, "", INK, w=1100, h=200),
                img("clock", "assets/clock.png", 1937, 1062, 85)]
    mixed = [disc(f"mg{i}", x, y, 56, FAINT, GRAYP, 3) for i, (x, y) in enumerate(
        [(1255, 340), (1930, 315), (1818, 458), (1678, 585), (1826, 725)])]
    mixed += [disc("mt", 1372, 240, 56, TEAL, RING, 3.5), disc("mo", 1497, 600, 56, OLIVE, RING, 3.5),
              disc("mb", 1305, 474, 56, COOL, RING, 3.5, dashed=True), disc("md", 1755, 355, 56, DEEP, RING, 3.5, dashed=True),
              disc("mk", 1545, 425, 56, HOT, RING, 3.5, dashed=True), disc("mq", 1523, 466, 56, HOT, INK, 3.5),
              aro("ma1", (1395, 270), (1437, 330), TEAL, w=4), aro("ma2", (1500, 570), (1520, 535), OLIVE, w=4),
              aro("ma3", (1498, 400), (1470, 378), HOT, True, 4), aro("ma4", (1500, 470), (1415, 474), HOT, False, 4),
              aro("ma5", (1555, 450), (1635, 420), HOT, False, 4), aro("ma6", (1525, 495), (1531, 525), HOT, False, 4),
              aro("ma7", (1330, 474), (1380, 480), COOL, True, 4), aro("ma8", (1730, 372), (1680, 390), DEEP, True, 4),
              text("mkl", "k<sub>i</sub>", 1565, 355, 40, "mi", INK, w=200), text("mql", "q<sub>i</sub>", 1455, 520, 40, "mi", INK, w=200)]
    add(stage(*scatter("nm", key_visible=True), *nm_extra, *mixed), cls="L-g")


def build(add):
    build_a1(add)
    build_a2(add)
    focus(add)
    build_b(add)
