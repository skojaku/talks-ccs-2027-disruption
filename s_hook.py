"""Slides 1-23: the title, the paper, the light bulb, the quotation, "my age", the two timelines."""
from mm import *  # noqa: F401,F403
import mm


def tl_plain():
    """Slides 12-16: one hand-drawn line with a ring at each end."""
    return [line("tl", 100, 330, 1895, 335, INK, 3.2, head=False),
            disc("tl_l", 102, 330, 24, "#fff", INK, 3.2), disc("tl_r", 1895, 335, 24, "#fff", INK, 3.2)]


def tl_two(xl, xm, xr, y, th, rd, rw):
    """Slides 21-23: orange before the turn, blue after it, three rings. Sizes in O units / px."""
    return [line("tl", xl, y, xm, y, HOT, th, head=False),
            line("tl2", xm, y, xr, y, DEEP, th, head=False),
            disc("tl_l", xl, y, rd, "#fff", HOT, rw), disc("tl_m", xm, y, rd, "#fff", DEEP, rw),
            disc("tl_r", xr, y, rd, "#fff", DEEP, rw)]


def build(add):
    # ---- 0  we live in the future we once imagined (two stills of Back to the Future Part II) -------------------------------
    add(PENCIL + h2("We live in the future we once imagined.")
        + stage(img("bttf_poster", "assets/bttf2_poster.jpg", 620, 640, 560, None, "ph"),
                img("bttf_phone", "assets/bttf2_phone.jpg", 1330, 640, 670, None, "ph"))
        + '\n\n<div class="ref">Back to the Future Part II (Universal Pictures, 1989): theatrical poster and a still.</div>',
        cls="L-b", header="",
        notes="Opening: the 1989 film imagined 2015. Smart glasses, video calls and flat screens are now ordinary.")

    # ---- 2  the paper this talk is about (part opener: title, authors, faces) -------------------------------------
    add("""## Uncovering simultaneous scientific breakthroughs with a robust measure of disruptiveness

<p>Munjung Kim, Sadamori Kojaku, Yong-Yeol Ahn. Science Advances.</p>

<div class="faces">
<figure><img src="assets/face_munjung.png" style="border-radius:50%"><figcaption>Munjung Kim</figcaption></figure>
<figure><img src="assets/face_sadamori.jpg"><figcaption>Sadamori Kojaku</figcaption></figure>
<figure><img src="assets/face_ahn.jpg"><figcaption>Yong-Yeol Ahn</figcaption></figure>
</div>

<div class="faces" style="gap:40px;align-items:center">
<img src="assets/logo_uva.png" style="height:70px"><img src="assets/logo_binghamton.png" style="height:70px"><img src="assets/logo_afosr.png" style="height:70px">
</div>""", cls="part", header="",
        notes="The paper behind this talk. Ask the room how they would measure that a paper is disruptive.")

    # ---- 3-5  the technology collage and the light bulb -----------------------------------------------
    def collage(pos):
        o = []
        o.append(img("phone", "assets/phone.png", *pos["phone"]))
        o.append(img("chat", "assets/chatgpt.png", *pos["chat"], cls="ph"))
        o.append(img("globe", "assets/globe.png", *pos["globe"], cls="ph"))
        o.append(img("printer", "assets/printer.jpg", *pos["printer"], cls="ph"))
        return o

    P3 = dict(phone=(772, 470, 245, 470), chat=(1550, 540, 600, 337), globe=(363, 827, 473, 473),
              printer=(1170, 862, 534, 356))
    P4 = dict(phone=(440, 305, 245, 470), chat=(989, 357, 597, 336), globe=(301, 826, 472, 472),
              printer=(899, 825, 532, 355))
    edison = lambda: img("edison", "assets/edison.jpg", 1690, 694, 555, 498, "ph")

    add(h2("Your most memorable technology?") + '\n\n<p class="sub">A shift, or a new technology, in your life.</p>' + stage(*collage(P3)), cls="L-b", header="")
    add(stage(*collage(P4), edison(), text("lbt", "Light bulb", 1690, 368, 44, weight=700)), cls="L-g")
    LB = "Light bulb changed human world"

    # the light bulb slide: house layout C, the three bullets are `*` fragments (one click each, on this one slide);
    # the photo morphs from the collage
    B = ["4–6 more hours a day", "The 24-hour economy", "Evening entertainment culture"]
    mm._names.append("edison")
    add(h2(LB, "lbt") + '\n\n<p class="sub">more than you’d think</p>\n\n<div class="cols">\n<div>\n\n'
        + "".join(f"* {t}\n" for t in B)
        + '\n</div>\n<div class="fig photo" style="view-transition-name:edison">\n\n![](assets/edison.jpg)\n\n</div>\n</div>',
        cls="L-c left")
    # the other technologies come back
    add(stage(*collage(P4), edison()), cls="L-g")

    # ---- 10-12  Douglas Adams (the portrait stays; the words change) ----------------------------------
    def adams(quote, who='“The Salmon of Doubt”, Douglas Adams'):
        return f"""<div class="cols">
<div>
<blockquote>

{quote}

</blockquote>
<p class="who">{who}</p>
</div>
<div class="fig" style="view-transition-name:adams">

![](assets/adams.jpg)

</div>
</div>"""

    mm._names.append("adams")
    add(adams('<span class="hot">Anything that is in the world when you’re born is normal</span> and ordinary and is '
              'just a natural part of the way the world works.'), cls="L-q")
    mm._names.append("adams")
    add(adams('<span class="hot">Anything that’s invented between when you’re fifteen and thirty-five is new and '
              'exciting</span> and revolutionary and you can probably get a career in it.'), cls="L-q")
    mm._names.append("adams")
    add(adams('Anything invented after you’re thirty-five is against the natural order of things.'), cls="L-q")

    # ---- 13-17  my age ----------------------------------------------------------------------------------
    age_title = h2('<span class="muted">My age</span>')

    def my_age(k):
        o = tl_plain()
        for i, (x, y, t) in enumerate([(277, 262, "6y old"), (785, 270, "12y old"), (1220, 265, "19y old"),
                                       (1715, 270, "36y old")]):
            o.append(text(f"age{i}", t, x, y, 32, "", MUTED, w=420, weight=700, style="font-style:italic;"))
        cols = [
            ("Pagers", 280, 480, ("pager", "assets/pager.png", 292, 740, 460), ("This was normal", 268, 1015),
             (268, 975, 268, 918, 0)),
            ("Wireless phone", 830, 480, ("nokia", "assets/nokia3310.png", 800, 740, 500), ("Innovative 🤯", 790, 1015),
             (840, 975, 870, 895, 0.25)),
            ("Smart phone", 1250, 480, ("phone", "assets/phone.png", 1246, 735, 198, 380), ("super cool!", 1210, 1015),
             (1237, 985, 1237, 937, 0)),
            ("Smart glass", 1735, 480, ("glasses", "assets/glasses.jpg", 1720, 735, 380, 363),
             ("Goes against<br>natural order", 1700, 1000), (1727, 960, 1710, 925, 0)),
        ]
        for i in range(k):
            lab, lx, ly, im, (atxt, ax, ay), (x1, y1, x2, y2, bend) = cols[i]
            fade = "opacity:.3;" if i < k - 1 else ""        # the past stays, faded
            o.append(text(f"era{i}", lab, lx, ly, 32, "", MUTED, w=520, style="font-style:italic;" + fade))
            nm, src, cx, cy, w, *hh = im
            o.append(img(nm, src, cx, cy, w, hh[0] if hh else None, "ph" if nm == "glasses" else "", fade))
            o.append(text(f"as{i}", atxt, ax, ay, 34, "aside", w=700, h=160 if "<br>" in atxt else 110, style=fade))
            o.append(overlay_svg(f"ar{i}", [curved_arrow(x1 * S, y1 * S, x2 * S, y2 * S, bend, MUTED, 2.4, 14)], style=fade))
        return o

    for k in (0, 1, 2, 3, 4):
        add(age_title + stage(*my_age(k)), cls="L-b")

    # ---- 18  the phones: before and after the turn -----------------------------------------------------
    flip = img("flip", "assets/flip.png", 690, 700, 470, None, "", "transform:rotate(46deg);")
    add(stage(
        *tl_two(112, 862, 1895, 330, 6, 46, 5),
        img("nokia", "assets/nokia3310.png", 205, 730, 390),
        img("nokia_teal", "assets/nokia_teal.png", 470, 725, 230, 388),
        flip,
        img("iphone", "assets/iphone.png", 1177, 700, 350, 616),
        img("docomo", "assets/docomo3.png", 1545, 705, 420),
        img("phone", "assets/phone.png", 1865, 700, 225, 430)), cls="L-g")

    # ---- 19  the same line, atomic models ----------------------------------------------------------------
    def caps(prefix, items, size=30):
        return [text(f"{prefix}{i}", f"{a}<br>{b}", cx, cy, size, w=520, h=160) for i, (a, b, cx, cy) in enumerate(items)]

    add(stage(
        *tl_two(112, 862, 1895, 330, 6, 46, 5),
        img("bohr", "assets/bohr.png", 270, 660, 460),
        img("vegard", "assets/vegard.png", 780, 650, 430),
        img("schrod", "assets/schrodinger.png", 1440, 670, 600, None, "ph"),
        *caps("cap", [("Bohr’s model", "(1913)", 270, 960), ("Vegard’s model", "(1918)", 780, 960),
                      ("Schrödinger’s model", "(1926)", 1440, 990)])), cls="L-g")

    # ---- 20  how can we quantify the disruptiveness ----------------------------------------------------
    add(h2('How do we <span class="hot">quantify</span> disruptiveness?') + stage(
        *tl_two(328, 908, 1713, 543, 4.5, 34, 4),
        img("bohr", "assets/bohr.png", 360, 750, 330),
        img("vegard", "assets/vegard.png", 800, 745, 310),
        img("schrod", "assets/schrodinger.png", 1440, 765, 430, None, "ph"),
        *caps("cap", [("Bohr’s model", "(1913)", 360, 965), ("Vegard’s model", "(1918)", 800, 965),
                      ("Schrödinger’s model", "(1926)", 1440, 990)])), cls="L-b")
