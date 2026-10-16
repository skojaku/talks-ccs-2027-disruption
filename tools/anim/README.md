# Animation review page (claude.ai artifact)

Rebuild when slides change:

1. `python3 build.py --html`, serve the project (`python3 -m http.server 8766`), run `node tools/anim/geo.mjs` (writes `geo_raw.json`; needs puppeteer-core from marp-cli).
2. Build `pairs.json` from `geo_raw.json` and `review/transitions.json`: per slide pair, every named object with its before/after box (x, y, w, h in 1280x720 px), `mv` (box changed), group label from `build.py` LABELS.
3. Artifact folder: `index.html` = `page.html` with `/*DATA*/` replaced by `pairs.json`; `s/NNN.jpg` (1024x576 slide images); `deck/index.html` = `ccs-2027.html` with `listener.js` inlined before `</body>`, plus the `assets/` and `figures/` it references.
4. Publish with the Artifact tool (capability `db`). Annotations land in collection `anim`, doc `tNNN` (NNN = slide before the transition).
