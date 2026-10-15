#!/usr/bin/env python3
"""Side-by-side sheet: original Keynote page (left) vs our render (right).
    python3 tools/compare.py <scratch> <first-orig-page> <first-our-slide> <count> <out.png> [map]
`map` is a comma list "ours:orig" overrides, e.g. "10:11,11:13" (our slide : original page).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
S = Path(sys.argv[1]); o0 = int(sys.argv[2]); s0 = int(sys.argv[3]); n = int(sys.argv[4]); out = sys.argv[5]
amap = dict(kv.split(":") for kv in sys.argv[6].split(",")) if len(sys.argv) > 6 and sys.argv[6] else {}
root = Path(__file__).resolve().parent.parent / "review"
W, H = 560, 315
sheet = Image.new("RGB", (W * 2 + 30, n * (H + 24)), (170, 170, 170))
d = ImageDraw.Draw(sheet)
for i in range(n):
    si = s0 + i
    oi = int(amap.get(str(si), o0 + i))
    a = Image.open(S / "orig" / f"o-{oi:02d}.png").convert("RGB").resize((W, H))
    b = Image.open(root / f"slide.{si:03d}.png").convert("RGB").resize((W, H))
    y = i * (H + 24)
    d.text((6, y + 4), f"original p{oi}", fill=(0, 0, 0)); d.text((W + 36, y + 4), f"ours s{si}", fill=(0, 0, 0))
    sheet.paste(a, (0, y + 20)); sheet.paste(b, (W + 30, y + 20))
sheet.save(out)
