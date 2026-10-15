"""Slides 36-54: word2vec, the query and key vectors, training by negation."""
import math

from mm import *  # noqa: F401,F403
import mm

# ---- the sketched network: 5 input nodes, 2 hidden, 5 output (local units; the drawing is 452 x 524) --------------
NW, NH = 452, 524
NX = (40, 226, 413)
IN_Y = [39, 137, 237, 339, 483]
HID_Y = [204, 340]
NR = 38


def net_body(color=INK, w=2.7):
    parts = []
    nodes = [(NX[0], y) for y in IN_Y] + [(NX[1], y) for y in HID_Y] + [(NX[2], y) for y in IN_Y]

    def arrow(a, b, key):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        return pencil_arrow(a[0] + ux * (NR + 2), a[1] + uy * (NR + 2), b[0] - ux * (NR + 5), b[1] - uy * (NR + 5),
                            key, color, w, 15)

    for i, y in enumerate(IN_Y):
        for h, hy in enumerate(HID_Y):
            parts.append(arrow((NX[0], y), (NX[1], hy), ("i", i, h)))
    parts.append(arrow((NX[1], HID_Y[0]), (NX[1], HID_Y[1]), "hh"))
    for h, hy in enumerate(HID_Y):
        for o, y in enumerate(IN_Y):
            parts.append(arrow((NX[1], hy), (NX[2], y), ("o", h, o)))
    for k, (x, y) in enumerate(nodes):
        parts.append(pencil_circle(x, y, NR, ("n", k), color, 3.4, "#fff"))
    return "".join(parts)


def net(name, cx, cy, s, color=INK, opacity=1.0):
    """The network centred on (cx, cy) in O units at scale s."""
    w, h = NW * s, NH * s
    return svg(name, cx - w / 2, cy - h / 2, w, h, net_body(color), NW, NH, "",
               f"opacity:{opacity};" if opacity != 1 else "")


def NP(cx, cy, s):
    """local network point -> slide px, for strokes drawn over the network."""
    return lambda lx, ly: ((cx + (lx - NW / 2) * s) * S, (cy + (ly - NH / 2) * s) * S)


def build(add):
    # ---- 36  word2vec ----------------------------------------------------------------------------------------------
    add(h2("word2vec") + stage(net("net", 1045, 607, 1.0)), cls="L-b", header="")

    # ---- 37-39  fox -> a vector ------------------------------------------------------------------------------------
    def fox(extra=()):
        return [net("net", 1046, 440, 0.735),
                text("fx", "“fox”", 545, 440, 52, weight=700, w=420),
                overlay_svg("fx_ar", [f'<path d="M442,276 L536,276" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                                      f'<path d="M520,266 L538,276 L520,286" fill="none" stroke="{INK}" stroke-width="3" '
                                      f'stroke-linecap="round" stroke-linejoin="round"/>'
                                      f'<path d="M790,280 L880,280" stroke="{COOL}" stroke-width="3" stroke-linecap="round"/>'
                                      f'<path d="M864,270 L882,280 L864,290" fill="none" stroke="{COOL}" stroke-width="3" '
                                      f'stroke-linecap="round" stroke-linejoin="round"/>']),
                text("fxv", "[1.2,0.3,−1]", 1680, 440, 44, "", COOL, weight=700, w=640), *extra]

    T = h2("word2vec (Mikolov et al. 2013)")
    add(T + stage(*fox()), cls="L-b")
    add(T + stage(*fox([
        text("m1", 'Learns by <span class="hot">metonymy</span>', 1045, 715, 38, weight=700, w=1200),
        text("m2", "Words that appear together sit<br>close in the vector space.", 1045, 842, 30, w=1500, h=160)])),
        cls="L-b")
    add(T + stage(*fox([
        text("m1", 'Learns by <span class="hot">metonymy</span>', 1045, 715, 38, weight=700, w=1200),
        text("m2", "Words that appear together sit<br>close in the vector space.", 1045, 842, 30, w=1500, h=160)]))
        + '\n\n<p class="take">Surprisingly effective. <span class="hot">Paradigm shift</span> in NLP</p>', cls="L-b")

    # ---- 40  analogies --------------------------------------------------------------------------------------------
    V = lambda w: f'<span class="vec">{w}</span>'
    eq = lambda a, b, c, d: f"{V(a)} − {V(b)} + {V(c)} = {V(d)}"
    add(h2('Learn by metonymy but captures <span class="hot">metaphor</span>.') + stage(
        text("an_a", eq("“man”", "“king”", "“woman”", "“queen”"), 1050, 500, 38, w=1700),
        text("an_b", eq("“Madrid”", "“Spain”", "“Japan”", "“Tokyo”"), 1050, 700, 38, w=1700),
        text("an_c", eq("“Taylor_Swift”", "“USA”", "“Japan”", "“Namie_Amuro”"), 1050, 1000, 32, "", MUTED, w=1900),
        text("an_t", "Tested 10y&gt; ago by myself", 1060, 855, 32, "aside", w=1300)), cls="L-b")

    # ---- 41-48  how word2vec works ---------------------------------------------------------------------------------
    foot = text("foot", "*word2vec has multiple variants. We focus on the skip-gram negative sampling word2vec.",
                1000, 1085, 22, "", MUTED, w=2000)
    NET = lambda color=INK, op=1.0: net("net", 1026, 730, 1.0, color, op)
    ttl = h2("How word2vec works")
    sent = lambda: [text("sent", '“Chance <span class="hot">favors</span> only the _____ mind.”', 980, 265, 48, w=1900),
                    overlay_svg("sent_ar", [curved_arrow(440, 128, 870, 124, -0.22, HOT, 4, 20)])]
    lab_f = lambda: text("lf", "“favors”", 655, 610, 40, "", HOT, w=560)
    lab_p = lambda: text("lp", "“prepared”", 1440, 802, 40, "", COOL, w=640, align="left")
    lab_p = lambda: text("lp", "“prepared”", 1285, 802, 40, "", COOL, w=640, align="left")
    add(ttl + stage(NET(), foot), cls="L-b", header="")
    add(stage(NET(), foot, *sent()), cls="L-g")
    add(stage(NET(), foot, *sent(), lab_f()), cls="L-g")
    add(stage(NET(), foot, *sent(), lab_f(), lab_p()), cls="L-g")
    add(stage(NET(), foot, lab_f(), lab_p()), cls="L-g")

    P = NP(1026, 730, 1.0)

    def br(pts, color, w=10):
        return brush_path([P(*p) for p in pts], color, w)

    qV = [br([(83, 147), (182, 322)], HOT), br([(83, 147), (176, 189)], HOT)]
    kV = [br([(260, 204), (365, 324)], COOL), br([(260, 329), (365, 329)], COOL)]
    qmat = ("$$q_{\\text{favor}}=\\begin{bmatrix}0.1\\\\-0.2\\end{bmatrix}$$")
    kmat = ("$$k_{\\text{prepare}}=\\begin{bmatrix}0.2\\\\0.1\\end{bmatrix}$$")
    qparts = lambda: [mathbox("qm", 40, 100, 650, 250, qmat, 46),
                      text("qn1", "N1", 700, 160, 30, "", INK, w=100, align="left"),
                      text("qn2", "N2", 700, 280, 30, "", INK, w=100, align="left"),
                      line("qu", 80, 353, 725, 351, HOT, 5, False),
                      text("ql", "query vector", 385, 405, 40, "", HOT, w=800)]
    kparts = lambda: [mathbox("km", 1130, 100, 700, 250, kmat, 46),
                      text("kn1", "N1", 1850, 150, 30, "", INK, w=100, align="left"),
                      text("kn2", "N2", 1850, 270, 30, "", INK, w=100, align="left"),
                      line("ku", 1200, 343, 1840, 341, COOL, 5, False),
                      text("kl", "key vector", 1520, 395, 40, "", COOL, w=800)]
    add(stage(NET(), foot, lab_f(), lab_p(), overlay_svg("qv", qV), *qparts()), cls="L-g")
    add(stage(NET(), foot, lab_f(), lab_p(), overlay_svg("qv", qV), overlay_svg("kv", kV), *qparts(), *kparts()),
        cls="L-g")

    # ---- 49  a word has two vectors --------------------------------------------------------------------------------
    kV2 = [br([(270, 195), (372, 148)], COOL, 10), br([(268, 310), (365, 182)], COOL, 10)]
    add(h2('A word has <span class="hot">two</span> vectors') + stage(
        NET(MUTED, 0.55), overlay_svg("qv", qV), overlay_svg("kv2", kV2),
        text("lf", "“favors”", 655, 610, 40, "", HOT, w=560),
        text("lf2", "“favors”", 1285, 610, 40, "", COOL, w=640, align="left"),
        text("lp", "“prepared”", 1285, 802, 40, "", COOL, w=640, align="left", style="opacity:.3;"),
        text("bq", "Query", 245, 625, 80, "", HOT, weight=700, w=640),
        text("bk", "Key", 1785, 625, 80, "", COOL, weight=700, w=640)), cls="L-b")

    # ---- 50-55  trained by negation ----------------------------------------------------------------------------------
    TT = h2("Trained by negation.")
    DOTS = {"g0": (1141, 349), "g1": (1265, 371), "g2": (1167, 500), "g3": (1167, 659), "g4": (1360, 684), "g5": (920, 833)}
    KEY, QRY, WAT = (1046, 371), (992, 677), (1376, 470)

    def left():
        return [net("net", 312, 705, 0.74),
                text("ls", '“… <span class="hot">favors</span> only the <span class="cool" style="text-decoration:underline">'
                           'prepared</span>”', 300, 462, 22, w=900),
                overlay_svg("ls_ar", [curved_arrow(72, 288, 270, 283, -0.4, HOT, 2.6, 13)]),
                img("ap1", "assets/apoha_stone.png", 1299, 125, 193),
                img("ap2", "assets/apoha_carved.png", 1523, 125, 173),
                img("ap3", "assets/apoha_horse.png", 1787, 125, 208),
                line("ax_y", 643, 1033, 643, 770, INK, 3.4, True, False, 16),
                line("ax_x", 641, 1033, 848, 1033, INK, 3.4, True, False, 16)]

    def dots(key=False, qry=False, water=False):
        o = []
        for nm, (x, y) in DOTS.items():
            o.append(disc(f"d_{nm}", x, y, 50, FAINT, "#E2DEDA", 3))
        o.append(disc("d_key", *KEY, 50, COOL if key else FAINT, INK if key else "#E2DEDA", 3.5 if key else 3))
        o.append(disc("d_qry", *QRY, 50, HOT if qry else FAINT, INK if qry else "#E2DEDA", 3.5 if qry else 3))
        o.append(disc("d_wat", *WAT, 50, "#A9A5A2" if water else FAINT, INK if water else "#E2DEDA", 3.5 if water else 3))
        return o

    kl = lambda: [text("kl1", "prepared<br>(key)", 842, 290, 30, "", COOL, w=420, h=130),
                  text("ql1", "favor<br>(query)", 1072, 775, 30, "", HOT, w=420, h=130)]
    wl = lambda: [text("wl1", "water<br>(random key)", 1435, 575, 30, "", MUTED, w=520, h=130),
                  text("wl2", "a randomly<br>sampled word", 1600, 820, 30, "", INK, w=520, h=130, align="left"),
                  overlay_svg("wl_ar", [f'<path d="M1066,476 L1000,408" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                                        f'<path d="M1003,426 L998,406 L1018,411" fill="none" stroke="{INK}" stroke-width="3" '
                                        f'stroke-linecap="round" stroke-linejoin="round"/>']),
                  mathbox("rj", 1540, 900, 400, 160, "$$r(j)$$", 46)]
    add(TT.replace("<h2", '<h2') + stage(*left(), *dots()), cls="L-b left")
    add(TT + stage(*left(), *dots(True, True), *kl()), cls="L-b left")
    add(TT + stage(*left(), *dots(True, True, True), *kl(), *wl()), cls="L-b left")
    mv = [line("mv1", *trim(*KEY, 1027, 478, 30, 0), COOL, 5, True, False, 22),
          line("mv2", *trim(*QRY, 1007, 567, 30, 0), HOT, 5, True, False, 22),
          line("mv3", *trim(*QRY, 904, 733, 30, 0), HOT, 5, True, False, 22),
          line("mv4", *trim(*WAT, 1468, 395, 30, 0), "#8C847F", 5, True, False, 22)]
    add(TT + stage(*left(), *dots(True, True, True), *kl(), *wl(), *mv), cls="L-b left")

    # ---- 54-55  the training table ----------------------------------------------------------------------------------
    def table(eqs=False):
        o = [text("th1", "query", 305, 100, 34, "", HOT, w=420), text("th2", "key", 667, 105, 34, "", COOL, w=420),
             text("th3", "dot sim<br>(x)", 1155, 112, 34, "", INK, w=520, h=150),
             text("th4", "genuine?<br>(y)", 1645, 112, 34, "", INK, w=520, h=150),
             line("tr1", 178, 182, 1807, 182, INK, 2, False), line("tr2", 178, 587, 1807, 587, INK, 2, False),
             text("r1q", "favor", 298, 257, 40, "", HOT, w=420), text("r1k", "prepared", 667, 255, 40, "", COOL, w=520),
             disc("r1qd", 297, 347, 50, HOT, INK, 3.5), disc("r1kd", 667, 347, 50, COOL, INK, 3.5),
             mathbox("r1x", 900, 215, 520, 160, "$q_{\\text{favor}}^\\top k_{\\text{prepare}}$", 40),
             text("r1y", "Yes (y=1)", 1645, 305, 40, "", INK, w=520),
             text("r2q", "favor", 308, 458, 40, "", HOT, w=420), text("r2k", "water", 667, 455, 40, "", MUTED, w=420),
             disc("r2qd", 308, 533, 50, HOT, INK, 3.5), disc("r2kd", 667, 530, 50, "#A9A5A2", INK, 3.5),
             mathbox("r2x", 900, 420, 520, 160, "$q_{\\text{favor}}^\\top k_{\\text{water}}$", 40),
             text("r2y", "No (y=0)", 1640, 503, 40, "", INK, w=520)]
        return o

    add(stage(*table()), cls="L-g")
    lg = [text("lg1", "Classify by the<br>logistic regression", 85, 755, 24, "", COOL, w=560, h=160, align="left"),
          text("lg2", "train by the log-<br>likelihood<br>maximization", 85, 950, 24, "", COOL, w=560, h=200, align="left"),
          mathbox("lg3", 660, 665, 1340, 190,
                  "$\\sigma_\\theta(i,j)=\\dfrac{1}{1+\\exp(-q_i^\\top k_j)}\\;\\;\\theta=\\{q_i,k_i\\}_{i=1}^{N}$", 30),
          mathbox("lg4", 640, 850, 1360, 190,
                  "$\\max_\\theta\\sum_{(i,j)\\in\\mathcal D}\\left[y_{i,j}\\log\\sigma_\\theta(i,j)+(1-y_{i,j})\\log(1-\\sigma_\\theta(i,j))\\right]$",
                  22)]
    add(stage(*table(), *lg), cls="L-g")
