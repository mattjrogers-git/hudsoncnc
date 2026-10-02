import sys; sys.path.insert(0, '/home/claude/logo')
from build import *

# faceted (straight-segment) ridge, x 0..1000, h 0..1000; tower at 735
FACET = [(0, 0), (130, 420), (215, 700), (262, 830), (300, 850), (360, 850), (395, 740), (470, 705), (530, 690), (556, 610),
         (585, 680), (650, 780), (705, 825), (765, 825), (830, 730), (900, 540), (960, 260), (1000, 0)]

def fpts(x0, y0, w, h):
    return [(x0 + X / 1000 * w, y0 - H / 1000 * h) for X, H in FACET]

def poly(pts, close_y=None):
    d = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    if close_y is not None:
        d += f' L{pts[-1][0]:.2f},{close_y:.2f} L{pts[0][0]:.2f},{close_y:.2f} Z'
    return d

def ftower(x0, y0, w, h, s):
    tx = x0 + 735 / 1000 * w; ty = y0 - 825 / 1000 * h + 2
    tw = s * 0.40
    return (f'M{tx - tw/2:.2f},{ty:.2f} V{ty - s*0.80:.2f} H{tx - tw*0.64:.2f} V{ty - s:.2f} H{tx + tw*0.64:.2f} '
            f'V{ty - s*0.80:.2f} H{tx + tw/2:.2f} V{ty:.2f} Z')

def crest_y(p, x):
    for (ax, ay), (bx, by) in zip(p, p[1:]):
        if ax <= x <= bx:
            return ay + (by - ay) * (x - ax) / (bx - ax) if bx > ax else ay
    return p[-1][1]

def facets(x0, y0, w, h, col, op, slit=None):
    """the Gunks cliffs: a pale band right under the crest on the cliffed stretches, with a few vertical cracks."""
    p = fpts(x0, y0, w, h); out = ''
    t = 0.13 * h
    for X0, X1 in ((205, 395), (585, 800)):
        xa = x0 + X0 / 1000 * w; xb = x0 + X1 / 1000 * w
        top = [(xa, crest_y(p, xa))] + [q for q in p if xa < q[0] < xb] + [(xb, crest_y(p, xb))]
        bot = [(x, y + t) for x, y in reversed(top)]
        # taper ends
        bot[0] = (bot[0][0] - w * 0.01, top[-1][1] + t * 0.35); bot[-1] = (bot[-1][0] + w * 0.01, top[0][1] + t * 0.35)
        out += f'<path d="{poly(top + bot)} Z" fill="{col}" opacity="{op}"/>'
        if slit:
            n = 6
            for i in range(1, n):
                x = xa + (xb - xa) * i / n + ((i * 37) % 7 - 3) * w * 0.002
                y = crest_y(p, x)
                out += f'<path d="M{x:.1f},{y + t*0.25:.1f} v{t*0.75:.1f}" stroke="{slit}" stroke-width="{max(1.5, w*0.004):.1f}" stroke-linecap="round"/>'
    return out

# ---------- E: round emblem
def concept_e(ink=INK, paper=PAPER, accent=BLUE):
    W = H = 800; cx = cy = 400
    body = f'<circle cx="{cx}" cy="{cy}" r="380" fill="{ink}"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="352" fill="none" stroke="{paper}" stroke-width="4"/>'
    rw = 560; x0 = cx - rw / 2; base = 470; rh = 230
    p = fpts(x0, base, rw, rh)
    body += f'<path d="{poly(p, base)}" fill="{accent}"/>'
    body += facets(x0, base, rw, rh, paper, 1, slit=accent)
    body += f'<path d="{ftower(x0, base, rw, rh, 52)}" fill="{paper}"/>'
    body += f'<rect x="{x0 - 40}" y="{base}" width="{rw + 80}" height="10" fill="{paper}"/>'
    d1, _ = text_path('HUDSON VALLEY', bsd(800), 92, cx, 590, tracking=0.03, anchor='middle')
    d2, _ = text_path('C N C', bsd(800), 70, cx, 668, tracking=0.08, anchor='middle')
    d3, _ = text_path('NEW PALTZ · NY', mono, 24, cx, 205, tracking=0.25, anchor='middle')
    body += f'<path d="{d1}" fill="{paper}"/><path d="{d2}" fill="{TAN}"/><path d="{d3}" fill="{paper}" opacity="0.8"/>'
    return svg(W, H, body)

# ---------- F: horizontal lockup, faceted mark in a rounded tile
def concept_f(ink=INK, paper=PAPER, accent=BLUE, bg=None):
    W, H = 1500, 400
    body = f'<rect x="20" y="40" width="320" height="320" rx="36" fill="{accent}"/>'
    rw = 280; x0 = 40; base = 290; rh = 150
    p = fpts(x0, base, rw, rh)
    body += f'<path d="{poly(p, base)}" fill="{INK}"/>' + facets(x0, base, rw, rh, PAPER, 1, slit=INK)
    body += f'<path d="{ftower(x0, base, rw, rh, 34)}" fill="{INK}"/>'
    body += f'<rect x="40" y="{base}" width="{rw}" height="8" fill="{paper}"/>'
    d1, _ = text_path('HUDSON VALLEY', bsd(800), 150, 390, 215, tracking=0.01)
    d2, w2 = text_path('CNC', bsd(800), 150, 390, 345, tracking=0.03)
    d3, _ = text_path('ROUTING · CARVING · FABRICATION', mono, 26, 390 + w2 + 34, 305, tracking=0.08)
    d4, _ = text_path('NEW PALTZ, NEW YORK', mono, 26, 390 + w2 + 34, 342, tracking=0.08)
    body += f'<path d="{d1}" fill="{ink}"/><path d="{d2}" fill="{accent}"/><path d="{d3}" fill="{ink}" opacity="0.75"/><path d="{d4}" fill="{ink}" opacity="0.75"/>'
    return svg(W, H, body, bg)

# ---------- G: name band under the ridge
def concept_g(ink=INK, paper=PAPER, accent=BLUE, bg=None):
    W, H = 1100, 520
    rw = 900; x0 = 100; base = 280; rh = 210
    p = fpts(x0, base, rw, rh)
    rf = ink if paper != INK else BLUE
    body = f'<path d="{poly(p, base)}" fill="{rf}"/>' + facets(x0, base, rw, rh, '#e9eae6', 1, slit=rf)
    body += f'<path d="{ftower(x0, base, rw, rh, 58)}" fill="{rf}"/>'
    body += f'<rect x="40" y="{base - 1}" width="1020" height="150" fill="{ink}"/>'
    d1, w1 = text_path('HUDSON VALLEY CNC', bsd(800), 128, 550, base + 122, tracking=0.03, anchor='middle')
    body += f'<path d="{d1}" fill="{paper}"/>'
    body += f'<rect x="40" y="{base + 160}" width="1020" height="10" fill="{accent}"/>'
    d2, _ = text_path('CNC ROUTING  ·  FABRICATION  ·  NEW PALTZ, NY', mono, 26, 550, base + 222, tracking=0.12, anchor='middle')
    body += f'<path d="{d2}" fill="{ink}" opacity="0.8"/>'
    return svg(W, H, body, bg)

O = '/home/claude/logo/out/'
open(O + 'E-emblem.svg', 'w').write(concept_e())
open(O + 'F-tile.svg', 'w').write(concept_f())
open(O + 'F-tile-reverse.svg', 'w').write(concept_f(ink=PAPER, paper=PAPER, accent='#2f6fd6', bg=INK))
open(O + 'G-band.svg', 'w').write(concept_g())
open(O + 'G-band-reverse.svg', 'w').write(concept_g(ink=PAPER, paper=INK, accent=TAN, bg=INK))
print('ok')
