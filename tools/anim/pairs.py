"""geo_raw.json (from geo.mjs) + build.py LABELS + review/transitions.json -> pairs.json for the animation review page. Run in the folder holding geo_raw.json."""
import json, re, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/Users/skojaku/Documents/projects/talks-ccs-2027-disruption'
src = open(ROOT + '/build.py').read()
a = src.index('LABELS = ['); b = src.index('\n]\n', a) + 3
ns = {}; exec(src[a:b], ns); LABELS = ns['LABELS']
def group(n):
    for pat, lab in LABELS:
        if re.search(pat, n): return lab
    return ''
g = json.load(open('geo_raw.json'))
tr = json.load(open(ROOT + '/review/transitions.json'))
R = lambda o: [round(o['x'], 1), round(o['y'], 1), round(o['w'], 1), round(o['h'], 1)]
def hint(o):
    return o['txt'][:28] if o['txt'] else (os.path.basename(o['img']) if o['img'] else '')
slides = [{o['name']: o for o in s['res']} for s in g]
pairs = []
for i in range(len(slides) - 1):
    A, B = slides[i], slides[i + 1]
    objs = []
    for n in sorted(set(A) | set(B), key=lambda n: (n not in A or n not in B, n)):
        oa, ob = A.get(n), B.get(n); o = ob or oa
        mv = bool(oa and ob and any(abs(x - y) > 1.0 for x, y in zip(R(oa), R(ob))))
        objs.append({'n': n, 'g': group(n), 'h': hint(o), 'b': R(oa) if oa else None, 'a': R(ob) if ob else None, 'mv': mv, 'abs': o['abs'],
                     'k': (o['cls'].split()[1] if o['cls'].startswith('o ') and len(o['cls'].split()) > 1 else o['tag'])})
    pairs.append(objs)
titles = []
for x in tr:
    ti = x['title']
    if len(ti) <= 3 or not ti: ti = ' / '.join(x['content'][:2])
    titles.append(ti[:60])
titles[0] = 'Title slide'
open('pairs.json', 'w').write(json.dumps({'titles': titles, 'pairs': pairs}, separators=(',', ':'), ensure_ascii=False))
print(len(titles), sum(1 for p in pairs if any(o['mv'] for o in p)))
