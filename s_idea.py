"""The big picture between the failure of the D-index and word2vec: look wider than the close neighbours, sample paths,
let word2vec turn the pairs into coordinates."""
import math
import random

from mm import *  # noqa: F401,F403
import mm
from s_walk import PAIRS, SEQ, pair
from s_w2v import net


def compressor(add):
    # ---- word2vec as an information compressor: the sequence of pairs on its left, the coordinates on its right -----------------------
    cols = [(0, 170), (1, 340), (4, 510), (6, 680)]
    pts = [(1560, 640, SEQ[0]), (1680, 540, SEQ[1]), (1770, 700, SEQ[2]), (1620, 770, SEQ[3]), (1500, 540, SEQ[4]), (1750, 600, SEQ[5])]
    add(h2("word2vec turns pairs into coordinates") + stage(
        text("pl", "(ancestor, descendant)", 430, 520, 36, "", INK, w=1000),
        *[pair(f"ip{i}", k, x, 640, 64) for i, (k, x) in enumerate(cols)],
        line("ia1", 790, 640, 900, 640, INK, 4, True, False, 20),
        text("inl", "word2vec", 1080, 380, 48, "", INK, weight=700, w=700),
        net("inet", 1080, 650, 0.72),
        text("ins", "an information compressor", 940, 970, 40, "aside", w=700),
        line("ia2", 1280, 640, 1380, 640, INK, 4, True, False, 20),
        line("sx", 1420, 860, 1860, 860, INK, 3.4, True, False, 16), line("sy", 1420, 860, 1420, 420, INK, 3.4, True, False, 16),
        *[disc(f"id{i}", x, y, 56, c, RING_, 3.5) for i, (x, y, c) in enumerate(pts)],
        text("itx", "a coordinate per node", 1650, 1040, 36, "", INK, w=700)), cls="L-b")


def onepaper(add):
    add(h2('Now, let’s look at <span class="hot">one paper</span> closely.'), cls="L-f", header="")


RING_ = "#4d4d4d"
