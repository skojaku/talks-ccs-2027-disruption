#!/usr/bin/env python3
"""assets/ic_phone.png, ic_printer.png, ic_chat.png: the technology collage drawn in the pencil touch of browser.png
(same wobble, same palette). Transparent background."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

K = 3
INK = (0, 0, 0, 255)
BLUE = (57, 89, 166, 255)
RED = (177, 68, 52, 255)
GOLD = (218, 177, 103, 255)
GREY = (166, 166, 166, 255)
PALE = (221, 227, 242, 255)
PEACH = (243, 221, 216, 255)
WHITE = (252, 252, 252, 255)
ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = Path.home() / "Library/Fonts/MesloLGS NF Bold.ttf"


class Sketch:
    def __init__(self, w, h, seed):
        self.W, self.H = w, h
        self.im = Image.new("RGBA", (w * K, h * K), (255, 255, 255, 0))
        self.d = ImageDraw.Draw(self.im)
        self.rng = random.Random(seed)

    def wob(self, pts, color=INK, w=6, passes=2, jit=2.2):
        for k in range(passes):
            q = [(x * K + self.rng.uniform(-jit, jit) * K, y * K + self.rng.uniform(-jit, jit) * K) for x, y in pts]
            self.d.line(q, fill=color, width=int((w - k) * K), joint="curve")

    @staticmethod
    def seg(a, b, n=14):
        return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n + 1)]

    @staticmethod
    def rr_pts(x0, y0, x1, y1, r):
        pts = []
        for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
            pts += [(cx + r * math.cos(math.radians(a0 + t * 9)), cy + r * math.sin(math.radians(a0 + t * 9))) for t in range(11)]
        pts.append(pts[0])
        return pts

    def rrect(self, x0, y0, x1, y1, r=24, fill=None, w=6, color=INK):
        pts = self.rr_pts(x0, y0, x1, y1, r)
        if fill:
            self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill)
        self.wob(pts, color, w)

    def circle(self, cx, cy, r, fill=None, w=5, color=INK):
        pts = [(cx + r * math.cos(math.radians(t * 12)), cy + r * math.sin(math.radians(t * 12))) for t in range(31)]
        if fill:
            self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill)
        self.wob(pts, color, w)

    def poly(self, pts, fill=None, w=5, color=INK, close=True):
        if fill:
            self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill)
        self.wob(pts + ([pts[0]] if close else []), color, w)

    def text(self, xy, s, size, color, anchor="la"):
        f = ImageFont.truetype(str(FONT), size * K) if FONT.exists() else ImageFont.load_default()
        self.d.text((xy[0] * K, xy[1] * K), s, fill=color, font=f, anchor=anchor)

    def save(self, name):
        im = self.im.filter(ImageFilter.GaussianBlur(0.4)).resize((self.W * K // 2, self.H * K // 2), Image.LANCZOS)
        im.save(ASSETS / name)
        print(name, im.size)


# ---- a smartphone ---------------------------------------------------------------------------------------------------
s = Sketch(520, 1000, 11)
s.rrect(24, 24, 496, 976, 78, WHITE, 7)
s.rrect(58, 110, 462, 884, 26, PALE, 5)
s.circle(260, 66, 13, INK, 3)
s.wob(s.seg((200, 934), (320, 934)), INK, 7, 1, 1.2)
cols = [RED, BLUE, GOLD, GREY]
for r in range(4):
    for c in range(3):
        x0 = 100 + c * 112
        y0 = 160 + r * 130
        s.rrect(x0, y0, x0 + 88, y0 + 88, 22, cols[(r + c) % 4], 4)
s.rrect(100, 700, 420, 780, 34, WHITE, 4)
s.wob(s.seg((140, 740), (300, 740)), GREY, 8, 1, 1.0)
s.save("ic_phone.png")

# ---- a 3D printer ---------------------------------------------------------------------------------------------------
s = Sketch(900, 600, 12)
s.rrect(40, 500, 860, 566, 18, GREY, 6)                     # base
s.rrect(150, 440, 750, 502, 12, PALE, 5)                    # bed
s.rrect(110, 70, 176, 502, 14, WHITE, 6)                    # posts
s.rrect(724, 70, 790, 502, 14, WHITE, 6)
s.rrect(110, 56, 790, 124, 18, WHITE, 6)                    # top beam
s.rrect(176, 190, 724, 232, 10, WHITE, 5)                   # gantry rail
s.rrect(396, 160, 504, 286, 16, RED, 6)                     # print head
s.poly([(436, 286), (464, 286), (450, 330)], GOLD, 4)       # nozzle
s.rrect(330, 352, 570, 444, 10, PALE, 5)                    # the printed object
for y in (372, 392, 412, 432):
    s.wob(s.seg((338, y), (562, y)), BLUE, 3, 1, 0.8)
s.text((450, 398), "3D", 62, BLUE, "mm")
s.circle(830, 190, 62, GOLD, 6)                             # filament spool
s.circle(830, 190, 20, WHITE, 5)
s.wob([(780, 150), (700, 112), (560, 150), (500, 200)], GOLD, 5, 1, 1.0)
s.save("ic_printer.png")

# ---- a chat window ---------------------------------------------------------------------------------------------------
s = Sketch(960, 540, 13)
s.rrect(24, 24, 936, 516, 40, WHITE, 7)
s.circle(96, 100, 30, PALE, 5, BLUE)
s.rrect(150, 64, 640, 188, 34, WHITE, 5)                    # reply
for i, wd in enumerate((420, 360, 250)):
    s.wob(s.seg((180, 94 + i * 34), (180 + wd, 94 + i * 34)), GREY, 9, 1, 1.0)
s.rrect(420, 220, 890, 318, 34, PALE, 5, BLUE)              # question
for i, wd in enumerate((380, 220)):
    s.wob(s.seg((450, 250 + i * 34), (450 + wd, 250 + i * 34)), BLUE, 9, 1, 1.0)
s.poly([(760, 130), (770, 150), (790, 160), (770, 170), (760, 190), (750, 170), (730, 160), (750, 150)], GOLD, 4)   # a spark
s.rrect(62, 380, 898, 476, 48, WHITE, 5)                    # the input bar
s.text((110, 428), "Ask anything", 40, GREY, "lm")
s.circle(836, 428, 34, BLUE, 4)
s.wob([(836, 446), (836, 410)], WHITE, 7, 1, 0.8)
s.wob([(818, 426), (836, 408), (854, 426)], WHITE, 7, 1, 0.8)
s.save("ic_chat.png")
