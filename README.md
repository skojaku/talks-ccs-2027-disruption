# ccs-2027: Marp deck with magic-move transitions

The Keynote talk `ccs-2027.key` (85 slides) rebuilt as a Marp deck in the house style (`~/.claude/skills/slide`).

    python3 tools/prep_assets.py <scratch>   # photos and plots cut out of ccs-2027.pdf into assets/ (needs pdfimages output, see script)
    python3 build.py --html                  # writes ccs-2027.md and ccs-2027.html

- **Present from `ccs-2027.html` in Chrome or Edge.** Objects that move in Keynote's Magic Move carry the same
  `view-transition-name` on consecutive slides and slide, grow or recolour between them (`MAGIC_MOVE.md`).
  Firefox and the PDF export show each slide's final state only.
- `mm.py` holds the drawing primitives; `s_hook.py`, `s_dindex.py`, `s_w2v.py`, `s_walk.py`, `s_end.py` the slides.
- `tools/compare.py` puts an original page next to our render for checking.
