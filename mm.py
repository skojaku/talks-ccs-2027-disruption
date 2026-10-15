"""Primitives for the magic-move stages of the deck.

Everything that has to move between two slides is an HTML box with a `view-transition-name`
(MAGIC_MOVE.md): a disc is a round div, an edge a thin rotated div, a picture a div around an <img>.
Positions are given in "O units", the 2000-px-wide space of the Keynote export that the original slides were read
in; `S` turns them into the 1280-px slide. Every object registers its name, so a slide can be checked for a
name used twice, and consecutive slides for the names they share (the objects that morph).
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
S = 0.64                      # O units -> slide px

INK, MUTED, PALE, FAINT = "#000000", "#6b6b6b", "#D9D9D9", "#EEEEEE"
HOT, COOL, GOLD, TEAL, OLIVE, DEEP = "#B14434", "#3959A6", "#DAB167", "#8FA3D6", "#DAB167", "#22336b"

FLOOR = 36                     # the type floor of the house style (px on the slide)
RAISED: list = []
_names: list[str] = []
_asp: dict[str, float] = {}


def take_names() -> list[str]:
    out = list(_names)
    _names.clear()
    return out


def _reg(name):
    if name:
        _names.append(name)
    return f"view-transition-name:{name};" if name else ""


def px(v):
    return f"{v * S:.2f}px"


def aspect(src: str) -> float:
    if src not in _asp:
        with Image.open(ROOT / src) as im:
            _asp[src] = im.size[0] / im.size[1]
    return _asp[src]


def box(name, x, y, w, h, inner="", cls="", style=""):
    """A box at (x, y) of size (w, h), all in O units."""
    return (f'<div class="o {cls}" style="left:{px(x)};top:{px(y)};width:{px(w)};height:{px(h)};'
            f'{_reg(name)}{style}">{inner}</div>')


def at(name, cx, cy, w, h, inner="", cls="", style=""):
    return box(name, cx - w / 2, cy - h / 2, w, h, inner, cls, style)


def img(name, src, cx, cy, w, h=None, cls="", style=""):
    """A picture centred on (cx, cy); the height follows the file unless given."""
    h = h or w / aspect(src)
    return at(name, cx, cy, w, h, f'<img src="{src}" alt="">', "pic " + cls, style)


def text(name, html, cx, cy, size, cls="", color=None, w=1400, h=None, align="center", weight=None,
         style="", family=None):
    """Text centred on (cx, cy) (O units); `size` is the font size in slide px."""
    if size < FLOOR and "foot" not in cls:
        RAISED.append((name, size))
        size = FLOOR
    h = h or size / S * 1.5
    if weight in (700, "700", "bold") and color in (HOT, COOL) and "ul-" not in html:
        html = f'<span class="ul-{"hot" if color == HOT else "cool"}">{html}</span>'      # a coloured value is underlined
    st = f"font-size:{size}px;"
    if color:
        st += f"color:{color};"
    if weight:
        st += f"font-weight:{weight};"
    if family:
        st += f"font-family:{family};"
    just = {"center": "center", "left": "flex-start", "right": "flex-end"}[align]
    if align == "left":
        x = cx
    elif align == "right":
        x = cx - w
    else:
        x = cx - w / 2
    return box(name, x, cy - h / 2, w, h, f"<span>{html}</span>", "tx " + cls,
               f"justify-content:{just};text-align:{align};{st}{style}")


def _gr(fill):
    """Coloured and grey fills get the pencil grain; white paper does not."""
    return "" if str(fill).lower() in ("#fff", "#ffffff", "white", "none") else "gr "


def disc(name, cx, cy, d, fill="#fff", ring=INK, rw=2.5, dashed=False, opacity=1.0, inner="", cls=""):
    """A round box of diameter d (O units)."""
    border = f"{rw}px {'dashed' if dashed else 'solid'} {ring}" if ring else "none"
    st = f"border-radius:50%;background:{fill};border:{border};box-sizing:border-box;"
    if opacity != 1:
        st += f"opacity:{opacity};"
    return at(name, cx, cy, d, d, inner, "dc " + _gr(fill) + cls, st)


def sq(name, cx, cy, s, fill=PALE, ring=None, rw=2, opacity=1.0, cls=""):
    border = f"{rw}px solid {ring}" if ring else "none"
    st = f"background:{fill};border:{border};box-sizing:border-box;"
    if opacity != 1:
        st += f"opacity:{opacity};"
    return at(name, cx, cy, s, s, "", "sq " + _gr(fill) + cls, st)


def dia(name, cx, cy, s, fill=DEEP, opacity=1.0, cls=""):
    """A diamond: a square of side s turned 45 degrees."""
    st = f"background:{fill};transform:rotate(45deg);"
    if opacity != 1:
        st += f"opacity:{opacity};"
    return at(name, cx, cy, s, s, "", "dm " + _gr(fill) + cls, st)


def line(name, x1, y1, x2, y2, color=INK, w=3.0, head=True, dashed=False, hs=None, opacity=1.0, cls=""):
    """A straight edge, drawn as a thin rotated div; the arrowhead is a CSS triangle at (x2, y2)."""
    X1, Y1, X2, Y2 = x1 * S, y1 * S, x2 * S, y2 * S
    L = math.hypot(X2 - X1, Y2 - Y1)
    a = math.degrees(math.atan2(Y2 - Y1, X2 - X1))
    hs = hs if hs is not None else max(7.0, w * 3.4)
    bg = (f"repeating-linear-gradient(90deg,{color} 0 {w * 2.2:.1f}px,transparent {w * 2.2:.1f}px {w * 4.2:.1f}px)"
          if dashed else color)
    st = (f"left:{X1:.2f}px;top:{Y1 - w / 2:.2f}px;width:{L:.2f}px;height:{w}px;background:{bg};"
          f"transform-origin:0 50%;transform:rotate({a:.2f}deg);--c:{color};--hs:{hs}px;")
    if opacity != 1:
        st += f"opacity:{opacity};"
    return f'<div class="o ln{" hd" if head else ""} {cls}" style="{st}{_reg(name)}"></div>'


def trim(x1, y1, x2, y2, a=0.0, b=0.0):
    """Shorten the segment (x1,y1)-(x2,y2) by a at the start and b at the end (O units)."""
    L = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    return x1 + ux * a, y1 + uy * a, x2 - ux * b, y2 - uy * b


def svg(name, x, y, w, h, body, vw=None, vh=None, cls="", style=""):
    """An SVG drawing inside a named div (the div is what the view transition captures)."""
    vw, vh = vw or w, vh or h
    return box(name, x, y, w, h,
               f'<svg viewBox="0 0 {vw} {vh}" width="100%" height="100%" preserveAspectRatio="none" '
               f'style="overflow:visible">{body}</svg>', cls, style)


def mathbox(name, x, y, w, h, tex, size=36, align="center", cls="", style="", color=None):
    """Markdown math in a named box. The blank lines let markdown-it (and KaTeX) see the formula."""
    st = f"font-size:{size}px;" + (f"color:{color};" if color else "")
    just = {"center": "center", "left": "flex-start", "right": "flex-end"}[align]
    return (f'<div class="o mx {cls}" style="left:{px(x)};top:{px(y)};width:{px(w)};height:{px(h)};'
            f'justify-content:{just};{st}{style}{_reg(name)}">\n\n{tex}\n\n</div>')


# ---- hand-drawn strokes (deterministic jitter) ---------------------------------------------------

def _rng(key):
    return random.Random(hash(key) & 0xFFFF if isinstance(key, int) else sum(map(ord, str(key))))


def pencil_circle(cx, cy, r, key, color=INK, w=2.4, fill="none"):
    """Two slightly offset, slightly wobbly strokes, as in the sketched networks."""
    rg = _rng(key)
    out = []
    for k in range(2):
        pts = []
        n = 14
        a0 = rg.uniform(0, 6.28)
        for i in range(n + 3):
            a = a0 + 6.2832 * i / n
            rr = r * (1 + rg.uniform(-0.035, 0.035))
            pts.append((cx + rr * math.cos(a) + rg.uniform(-0.8, 0.8), cy + rr * math.sin(a) + rg.uniform(-0.8, 0.8)))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" fill="{fill if k == 0 else "none"}" stroke="{color}" stroke-width="{w}" '
                   f'stroke-linejoin="round" stroke-linecap="round" opacity="{0.95 if k == 0 else 0.55}"/>')
    return "".join(out)


def pencil_arrow(x1, y1, x2, y2, key, color=INK, w=2.0, head=11):
    """A slightly bowed line with an open V arrowhead."""
    rg = _rng(key)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    bow = rg.uniform(-0.012, 0.012) * L
    mx, my = (x1 + x2) / 2 + nx * bow, (y1 + y2) / 2 + ny * bow
    ang = math.atan2(y2 - my, x2 - mx)
    hx = [(x2 - head * math.cos(ang - 0.42), y2 - head * math.sin(ang - 0.42)),
          (x2 - head * math.cos(ang + 0.42), y2 - head * math.sin(ang + 0.42))]
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{hx[0][0]:.1f},{hx[0][1]:.1f} L{x2:.1f},{y2:.1f} L{hx[1][0]:.1f},{hx[1][1]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def brush_path(pts, color, w, opacity=0.95):
    """A thick round-capped stroke through slide-px points (a hand brush), smoothed through the midpoints."""
    if len(pts) < 3:
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    else:
        mids = [((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2) for i in range(len(pts) - 1)]
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} L{mids[0][0]:.1f},{mids[0][1]:.1f}"
        for i in range(1, len(pts) - 1):
            d += f" Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mids[i][0]:.1f},{mids[i][1]:.1f}"
        d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return (f'<path class="shaft" pathLength="1" d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}"/>')


def curved_arrow(x1, y1, x2, y2, bend=0.25, color=MUTED, w=2.2, head=12):
    """A thin curved arrow (slide px) for asides; the shaft draws from its base, then the head pops."""
    dx, dy = x2 - x1, y2 - y1
    cx, cy = (x1 + x2) / 2 - dy * bend, (y1 + y2) / 2 + dx * bend
    ang = math.atan2(y2 - cy, x2 - cx)
    h1 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
    h2 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
    return (f'<path class="shaft" pathLength="1" d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path class="ahead" d="M{h1[0]:.1f},{h1[1]:.1f} L{x2:.1f},{y2:.1f} L{h2[0]:.1f},{h2[1]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow_px(x1, y1, x2, y2, color=INK, w=3.0, head=16):
    """A straight arrow in slide px: the shaft draws from (x1, y1), then the open head appears at (x2, y2)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    h1 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
    h2 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
    return (f'<path class="shaft" pathLength="1" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path class="ahead" d="M{h1[0]:.1f},{h1[1]:.1f} L{x2:.1f},{y2:.1f} L{h2[0]:.1f},{h2[1]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def overlay_svg(name, parts, cls="", style=""):
    """A full-slide transparent SVG layer (slide px coordinates) for arrows and brush strokes."""
    return (f'<div class="o ov {cls}" style="left:0;top:0;width:1280px;height:720px;{style}{_reg(name)}">'
            f'<svg viewBox="0 0 1280 720" width="1280" height="720">{"".join(parts)}</svg></div>')


# ---- slides ----------------------------------------------------------------------------------------

def stage(*objs):
    return '<div class="stage">' + "".join(objs) + "</div>"


def h2(html, name=None, style=""):
    return f'<h2 style="{_reg(name)}{style}">{html}</h2>'


def tri(name, cx, cy, w, h, color):
    """An upward triangle (the fulcrum of the seesaw), centred on (cx, cy)."""
    W, H = w * S, h * S
    return (f'<div class="o tri" style="left:{cx * S - W / 2:.2f}px;top:{cy * S - H / 2:.2f}px;width:0;height:0;'
            f'border-left:{W / 2:.2f}px solid transparent;border-right:{W / 2:.2f}px solid transparent;'
            f'border-bottom:{H:.2f}px solid {color};{_reg(name)}"></div>')


LAV = MUTED              # arrows and context edges are muted (HOUSE_STYLE section 3)
GRAYC = "#4d4d4d"        # a dark grey: "cites only the references" / the second diamond


def fade(objs, o=0.3):
    """The past stays, faded (HOUSE_STYLE 9.3): give every object in the list the opacity o."""
    return [x.replace('style="', f'style="opacity:{o};', 1) for x in objs]


PENCIL = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="mm-pencil" x="-10%" y="-10%" '
          'width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="7" result="n"/>'
          '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/></filter></svg>')
