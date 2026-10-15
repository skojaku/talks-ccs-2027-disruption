#!/usr/bin/env python3
"""assets/browser.png: a hand-drawn browser window (the 'internet' of the technology build), pencil style."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

K = 3
W, H = 900 * K, 680 * K
INK = (0, 0, 0)
BLUE = (57, 89, 166)
RED = (177, 68, 52)
GREY = (166, 166, 166)
rng = random.Random(5)
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)
FONT = Path.home() / "Library/Fonts/MesloLGS NF Bold.ttf"
font = ImageFont.truetype(str(FONT), 46 * K) if FONT.exists() else ImageFont.load_default()


def wob(pts, color=INK, w=4, passes=2, jit=2.2):
    for k in range(passes):
        q = [(x * K + rng.uniform(-jit, jit) * K, y * K + rng.uniform(-jit, jit) * K) for x, y in pts]
        d.line(q, fill=color, width=int((w - k) * K), joint="curve")


def seg(a, b, n=14):
    return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n + 1)]


def rrect(x0, y0, x1, y1, r=24, **kw):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        pts += [(cx + r * math.cos(math.radians(a0 + t * 9)), cy + r * math.sin(math.radians(a0 + t * 9))) for t in range(11)]
    pts.append(pts[0])
    wob(pts, **kw)


def circle(cx, cy, r, color=INK, w=4, fill=None):
    if fill:
        d.ellipse([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], fill=fill)
    wob([(cx + r * math.cos(math.radians(t * 12)), cy + r * math.sin(math.radians(t * 12))) for t in range(31)], color, w)


# the window and its title bar
d.rounded_rectangle([20 * K, 20 * K, 880 * K, 660 * K], radius=30 * K, fill=(250, 250, 250))
rrect(20, 20, 880, 660, 30, w=6)
wob(seg((20, 110), (880, 110)), w=5)
for i, c in enumerate((RED, (218, 177, 103), BLUE)):
    circle(68 + i * 52, 65, 15, INK, 4, c)
# address bar
d.rounded_rectangle([250 * K, 40 * K, 840 * K, 92 * K], radius=26 * K, fill="white")
rrect(250, 40, 840, 92, 26, w=4)
d.text((300 * K, 46 * K), "www", fill=BLUE, font=font)
# a globe
circle(240, 340, 130, BLUE, 6, (221, 227, 242))
wob([(240 + 130 * math.cos(math.radians(t * 12)) * 0.45, 340 + 130 * math.sin(math.radians(t * 12))) for t in range(31)], BLUE, 4)
wob(seg((110, 340), (370, 340)), BLUE, 4)
wob([(240 + 130 * math.cos(math.radians(a)) , 340 + 130 * math.sin(math.radians(a)) * 0.0 + (-65 if a == 0 else 0)) for a in (180, 210, 240, 270, 300, 330, 360)], BLUE, 0)
for yy in (-70, 70):
    r = math.sqrt(130 ** 2 - yy ** 2)
    wob(seg((240 - r, 340 + yy), (240 + r, 340 + yy)), BLUE, 3)
# page text and a picture block
for i, wd in enumerate((330, 290, 330, 220)):
    wob(seg((450, 220 + i * 52), (450 + wd, 220 + i * 52)), GREY, 9, 1, 1.0)
rrect(450, 440, 840, 610, 14, color=INK, w=4)
wob(seg((470, 585), (560, 500), 6) + seg((560, 500), (620, 550), 6) + seg((620, 550), (700, 470), 6) + seg((700, 470), (820, 590), 8), RED, 5)
circle(780, 490, 22, RED, 4, (243, 221, 216))
# links in blue under the globe
for i, wd in enumerate((250, 190)):
    wob(seg((115, 520 + i * 48), (115 + wd, 520 + i * 48)), BLUE, 7, 1, 1.0)
im = im.filter(ImageFilter.GaussianBlur(0.4)).resize((W // 2, H // 2), Image.LANCZOS)
im.save(Path(__file__).resolve().parent.parent / "assets/browser.png")
print(im.size)
