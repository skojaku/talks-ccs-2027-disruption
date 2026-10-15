"""The big picture between the failure of the D-index and word2vec: look wider than the close neighbours, sample paths,
let word2vec turn the pairs into coordinates."""
import math
import random

from mm import *  # noqa: F401,F403
import mm
from s_walk import PAIRS, SEQ, pair
from s_w2v import net


def compressor(add):
    # ---- word2vec as an information compressor: the pairs in one row, word2vec below, the coordinates to its right ----------------
    cols = [(0, 510), (1, 770), (4, 1030), (6, 1290)]
    pts = [(1460, 790, SEQ[0]), (1620, 700, SEQ[1]), (1760, 800, SEQ[2]), (1560, 900, SEQ[3]), (1730, 940, SEQ[4]), (1420, 940, SEQ[5])]
    add(h2("word2vec turns pairs into coordinates") + stage(
        text("pl", "(ancestor, descendant)", 900, 250, 36, "", INK, w=1000),
        *[pair(f"ip{i}", k, x, 360, 88) for i, (k, x) in enumerate(cols)],
        line("ia1", 900, 440, 900, 500, INK, 4, True, False, 20),
        text("inl", "word2vec", 900, 560, 48, "", INK, weight=700, w=700),
        net("inet", 900, 840, 0.62),
        text("ins", "an information compressor", 900, 1060, 40, "aside", w=1000),
        line("ia2", 1090, 840, 1300, 840, INK, 4, True, False, 20),
        line("sx", 1340, 1010, 1900, 1010, INK, 3.4, True, False, 16), line("sy", 1340, 1010, 1340, 640, INK, 3.4, True, False, 16),
        *[disc(f"id{i}", x, y, 56, c, RING_, 3.5) for i, (x, y, c) in enumerate(pts)],
        text("itx", "a coordinate per node", 1620, 570, 36, "", INK, w=800)), cls="L-b")


def onepaper(add):
    add(h2('Now, let’s look at <span class="hot">one paper</span> closely.'), cls="L-f", header="")


RING_ = "#4d4d4d"
