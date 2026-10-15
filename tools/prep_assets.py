#!/usr/bin/env python3
"""Extract the deck's photos, logos and screenshots from ccs-2027.pdf into assets/.

    python3 tools/prep_assets.py <scratch-dir>

<scratch-dir>/uniq/oNNN_pPP.png are the PDF's embedded images (pdfimages, soft masks merged; NNN is the
PDF object id). Keynote exports a drop shadow as its own white image, so those are skipped. The
vector plots (histograms, odds ratios) are not embedded images; they are cut from a 3x render of
their slide with pdftoppm.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SCRATCH = Path(sys.argv[1])
UNIQ = SCRATCH / "uniq"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
PDF = Path.home() / "Downloads" / "ccs-2027.pdf"


def load(obj):
    return Image.open(next(UNIQ.glob(f"o{obj:03d}_p*.png")))


def over_white(im):
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, im).convert("RGB")


def crop(im, x0, y0, x1, y1):
    w, h = im.size
    return im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))


def cutout(im, thresh=26, trim=True, feather=1.2):
    """Make the flat photo background transparent: flood-fill from the border with a colour tolerance,
    so light parts inside the object (white keys, the screen) stay opaque."""
    from PIL import ImageDraw, ImageFilter
    im = over_white(im).convert("RGB")
    w, h = im.size
    mark = (255, 0, 255)
    work = im.copy()
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    seeds += [(x, 0) for x in range(0, w, max(1, w // 24))] + [(x, h - 1) for x in range(0, w, max(1, w // 24))]
    seeds += [(0, y) for y in range(0, h, max(1, h // 24))] + [(w - 1, y) for y in range(0, h, max(1, h // 24))]
    for sd in seeds:
        if work.getpixel(sd) != mark:
            ImageDraw.floodfill(work, sd, mark, thresh=thresh)
    a = np.asarray(work)
    bgmask = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    alpha = Image.fromarray(np.where(bgmask, 0, 255).astype(np.uint8), "L")
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(feather))
    res = im.convert("RGBA")
    res.putalpha(alpha)
    if trim:
        box = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
        if box:
            pad = 6
            res = res.crop((max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, w), min(box[3] + pad, h)))
    return res


def save(im, name, jpg=False):
    if jpg:
        over_white(im).save(OUT / name, quality=92)
    else:
        im.save(OUT / name)


# ---- logos, QR, faces, the Science Advances paper -----------------------------------------------
save(load(9), "logo_binghamton.png")
save(load(8), "logo_afosr.png")
save(load(28), "logo_uva.png")
save(load(10), "qr.png")
save(load(27), "face_munjung.png")
save(load(25), "face_sadamori.jpg", jpg=True)
save(load(24), "face_ahn.jpg", jpg=True)
save(load(29), "sciadv.png")

# ---- the technology collage and the light bulb ---------------------------------------------------
save(load(55), "globe.png")
save(cutout(load(57)), "phone.png")
save(load(59), "chatgpt.png")
save(crop(load(61).convert("RGB"), 0.094, 0, 0.837, 1), "edison.jpg", jpg=True)
save(load(62), "printer.jpg", jpg=True)

# ---- the quotation -------------------------------------------------------------------------------
save(load(125), "adams.jpg", jpg=True)

# ---- "my age" and the phones -------------------------------------------------------------------
save(cutout(load(184), thresh=14), "pager.png")
save(cutout(load(195)), "nokia3310.png")
save(crop(load(220).convert("RGB"), 0, 0.03, 0.5, 0.87), "glasses.jpg", jpg=True)
save(cutout(crop(over_white(load(229)), 0.19, 0, 0.46, 1)), "nokia_teal.png")
save(cutout(load(230)), "flip.png")
save(cutout(load(231)), "iphone.png")
save(cutout(crop(load(232).convert("RGB"), 0, 0, 0.485, 0.47)), "docomo3.png")

# ---- atomic models -----------------------------------------------------------------------------
save(load(242), "bohr.png")
save(over_white(load(244)), "vegard.png")
save(over_white(crop(load(243), 0.79, 0.0, 1.0, 0.29)), "schrodinger.png")

# ---- the three papers ---------------------------------------------------------------------------
p296 = over_white(load(296))
save(crop(p296, 0.0, 0, 0.5, 1), "paper_team.png")
save(crop(p296, 0.5, 0, 1.0, 1), "paper_trend.png")
top = over_white(crop(load(299), 0, 0, 1, 0.62))
plot = over_white(load(300))
plot = plot.resize((top.size[0], round(plot.size[1] * top.size[0] / plot.size[0])))
comp = Image.new("RGB", (top.size[0], top.size[1] + plot.size[1] + 12), (255, 255, 255))
comp.paste(top, (0, 0))
comp.paste(plot, (0, top.size[1] + 12))
save(comp, "paper_remote.png")

# ---- Englert and Higgs; the APS pages ------------------------------------------------------------
h = over_white(load(311))
W, H = h.size
save(h.crop((538, 60, 538 + 1448, 60 + 1022)), "higgs.jpg", jpg=True)
save(load(914), "aps_news.png")
save(load(915), "prl.png")

# ---- the Apoha illustrations (without the labels) ----------------------------------------------

# ---- the last slide -----------------------------------------------------------------------------
save(load(1050), "butterfly.png")
save(load(1051), "avatar.jpg", jpg=True)
save(load(885), "clock.png")

# ---- vector plots: cut from a 3x render of their slide ------------------------------------------
R = 216  # dpi; the page is 72 dpi * 1920 pt wide, my slide coordinates are 2000 wide -> 1 unit = 2.88 px


def cut_page(page, box, name):
    x0, y0, x1, y1 = [round(v * 2.88) for v in box]
    stem = SCRATCH / f"pg{page}"
    subprocess.run(["pdftoppm", "-png", "-r", str(R), "-f", str(page), "-l", str(page), "-x", str(x0), "-y", str(y0),
                    "-W", str(x1 - x0), "-H", str(y1 - y0), "-singlefile", str(PDF), str(stem)], check=True)
    Image.open(str(stem) + ".png").convert("RGB").save(OUT / name)


cut_page(77, (405, 258, 1635, 1112), "hist_dindex.png")
cut_page(80, (850, 175, 1985, 1010), "hist_edm.png")
cut_page(83, (656, 308, 1893, 975), "odds_ratio.png")
print(sorted(p.name for p in OUT.iterdir()))
