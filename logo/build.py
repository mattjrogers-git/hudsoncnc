import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

F = '/home/claude/logo/fonts/'
_fonts = {}
def font(name, **axes):
    key = (name, tuple(sorted(axes.items())))
    if key not in _fonts:
        f = TTFont(F + name)
        if axes: f = instantiateVariableFont(f, axes)
        _fonts[key] = f
    return _fonts[key]

def text_path(s, f, size, x, y, tracking=0.0, anchor='start'):
    """return (svg path d, width) with baseline at y; tracking in em."""
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size / upm
    # width
    adv = []
    for ch in s:
        g = cmap.get(ord(ch))
        adv.append(gs[g].width if g else upm * 0.3)
    w = sum(adv) * sc + tracking * size * (len(s) - 1)
    if anchor == 'middle': x -= w / 2
    elif anchor == 'end': x -= w
    pen = SVGPathPen(gs); cx = x
    for ch, a in zip(s, adv):
        g = cmap.get(ord(ch))
        if g:
            tp = TransformPen(pen, (sc, 0, 0, -sc, cx, y))
            gs[g].draw(tp)
        cx += a * sc + tracking * size
    return pen.getCommands(), w

def cap_height(f, size):
    upm = f['head'].unitsPerEm
    return f['OS/2'].sCapHeight * size / upm

# --- Shawangunk ridge profile, seen from New Paltz looking west (south = left)
RIDGE = [(0, 0), (40, 90), (100, 260), (160, 470), (205, 640), (240, 760), (268, 830), (300, 850), (345, 852), (372, 820),
         (405, 735), (455, 700), (510, 690), (540, 650), (556, 600), (572, 640), (610, 720), (660, 785), (705, 820),
         (735, 830), (762, 815), (800, 760), (850, 700), (905, 610), (945, 470), (975, 260), (1000, 60)]
TOWER_X = 735

def ridge_pts(x0, y0, w, h, base=0, exag=1.0):
    """map ridge to box; y0 = baseline, h = height of tallest point above baseline."""
    hmax = max(p[1] for p in RIDGE)
    pts = []
    for X, H in RIDGE:
        pts.append((x0 + X / 1000 * w, y0 - (H - base) / (hmax - base) * h))
    return pts

def smooth_path(pts):
    # Catmull-Rom to cubic bezier
    d = f'M{pts[0][0]:.2f},{pts[0][1]:.2f}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        t = 0.18
        c1 = (p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t)
        c2 = (p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t)
        d += f' C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}'
    return d

def ridge_y_at(pts, x):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if ax <= x <= bx:
            t = (x - ax) / (bx - ax); return ay + (by - ay) * t
    return pts[-1][1]

def tower(pts, x0, w, s):
    """Sky Top tower: square stone tower with parapet, s = tower height."""
    tx = x0 + TOWER_X / 1000 * w; ty = ridge_y_at(pts, tx) + s * 0.08
    tw = s * 0.42
    d = (f'M{tx - tw/2:.2f},{ty:.2f} L{tx - tw/2:.2f},{ty - s*0.82:.2f} L{tx - tw*0.62:.2f},{ty - s*0.82:.2f} L{tx - tw*0.62:.2f},{ty - s:.2f} '
         f'L{tx + tw*0.62:.2f},{ty - s:.2f} L{tx + tw*0.62:.2f},{ty - s*0.82:.2f} L{tx + tw/2:.2f},{ty - s*0.82:.2f} L{tx + tw/2:.2f},{ty:.2f} Z')
    return d

def cliff_band(pts, x0, w, base, col, depth=None, step=None, sw=3, op=0.85, off=None):
    """pale line just under the crest = the white conglomerate cliffs of the Gunks."""
    if off is None: off = max(5, (base - min(p[1] for p in pts)) * 0.11)
    out = ''
    for X0, X1 in ((225, 385), (410, 545), (590, 790)):
        seg = []
        x = x0 + X0 / 1000 * w
        while x <= x0 + X1 / 1000 * w:
            seg.append((x, ridge_y_at(pts, x) + off)); x += 3
        out += 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in seg) + ' '
    return f'<path d="{out}" stroke="{col}" stroke-width="{sw}" opacity="{op}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

INK = '#16191c'; BLUE = '#1d58b8'; TAN = '#c9a46c'; PAPER = '#f4f5f2'

def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'

bsd = lambda wt: font('BigShouldersDisplay[wght].ttf', wght=wt)
mono = font('IBMPlexMono-Medium.ttf')
inst = lambda wt: font('InstrumentSans[wdth,wght].ttf', wght=wt, wdth=100)

# ---------- A: Ridgeline lockup (stacked)
def concept_a(ink=INK, accent=BLUE, bg=None, cliff=None, sub_op=0.8):
    W, H = 1000, 560
    d1, w1 = text_path('HUDSON VALLEY CNC', bsd(800), 150, 0, 0, tracking=0.01)
    sc = 860 / w1
    x0 = (W - 860) / 2
    pts = ridge_pts(x0, 300, 860, 150)
    poly = smooth_path(pts) + f' L{x0+860:.2f},300 L{x0:.2f},300 Z'
    body = f'<path d="{poly}" fill="{ink}"/><path d="{tower(pts, x0, 860, 44)}" fill="{ink}"/>'
    body += cliff_band(pts, x0, 860, 300, cliff or (TAN if bg else PAPER), sw=4, op=0.9)
    body += f'<rect x="{x0}" y="300" width="860" height="10" fill="{accent}"/>'
    dA, _ = text_path('HUDSON VALLEY CNC', bsd(800), 150 * sc, x0, 300 + 30 + cap_height(bsd(800), 150 * sc), tracking=0.01)
    body += f'<path d="{dA}" fill="{ink}"/>'
    dB, _ = text_path('CNC ROUTING  ·  FABRICATION  ·  NEW PALTZ, NY', mono, 26, W / 2, 520, tracking=0.12, anchor='middle')
    body += f'<path d="{dB}" fill="{ink}" opacity="{sub_op}"/>'
    return svg(W, H, body, bg)

# ---------- B: Toolpath (ridge drawn by an end mill)
def endmill(x, y, s, col):
    # bit tip at (x,y), pointing down; s = overall height
    w = s * 0.28; fl = s * 0.45
    d = f'M{x - w/2:.2f},{y - fl:.2f} L{x + w/2:.2f},{y - fl:.2f} L{x + w/2:.2f},{y - s*0.06:.2f} Q{x + w/2:.2f},{y:.2f} {x:.2f},{y:.2f} Q{x - w/2:.2f},{y:.2f} {x - w/2:.2f},{y - s*0.06:.2f} Z'
    flutes = ''
    for i in range(4):
        yy = y - fl + fl * (i + 0.3) / 4
        flutes += f'M{x - w/2:.2f},{yy:.2f} L{x + w/2:.2f},{yy + fl*0.16:.2f} '
    shank = f'M{x - w*0.36:.2f},{y - fl:.2f} L{x - w*0.36:.2f},{y - s:.2f} L{x + w*0.36:.2f},{y - s:.2f} L{x + w*0.36:.2f},{y - fl:.2f} Z'
    collar = f'M{x - w*0.62:.2f},{y - s*0.86:.2f} h{w*1.24:.2f} v{-s*0.14:.2f} h{-w*1.24:.2f} Z'
    return (f'<path d="{shank}" fill="{col}"/><path d="{collar}" fill="{col}"/><path d="{d}" fill="{col}"/>'
            f'<path d="{flutes}" stroke="#ffffff" stroke-width="{s*0.025:.2f}" opacity="0.55" fill="none"/>')

def concept_b(ink=INK, accent=BLUE, bg=None):
    W, H = 1500, 420
    rw = 400; x0 = 40
    pts = ridge_pts(x0, 300, rw, 120)
    # draw ridge up to tower position as a "cut" line; remainder dashed (toolpath not yet cut)
    cut = [p for p in pts if p[0] <= x0 + rw * 0.905]
    endp = cut[-1]
    body = f'<path d="{smooth_path(cut)}" fill="none" stroke="{accent}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    rest = [p for p in pts if p[0] >= endp[0]]
    body += f'<path d="{smooth_path(rest)}" fill="none" stroke="{accent}" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round" opacity="0.6"/>'
    body += f'<path d="{tower(pts, x0, rw, 36)}" fill="{accent}"/>'
    body += endmill(endp[0], endp[1] + 2, 140, ink)
    body += f'<rect x="{x0}" y="330" width="{rw}" height="5" fill="{ink}" opacity="0.25"/>'
    tx = x0 + rw + 70
    d1, _ = text_path('HUDSON VALLEY', bsd(800), 130, tx, 215, tracking=0.01)
    d2, w2 = text_path('CNC', bsd(800), 130, tx, 335, tracking=0.04)
    d3, _ = text_path('ROUTING · CARVING · FABRICATION', mono, 24, tx + w2 + 30, 300, tracking=0.08)
    d4, _ = text_path('NEW PALTZ, NEW YORK', mono, 24, tx + w2 + 30, 334, tracking=0.08)
    body += f'<path d="{d1}" fill="{ink}"/><path d="{d2}" fill="{accent}"/><path d="{d3}" fill="{ink}" opacity="0.75"/><path d="{d4}" fill="{ink}" opacity="0.75"/>'
    return svg(W, H, body, bg)

# ---------- C: Layered badge
def arc_text(s, f, size, cx, cy, r, start_deg, tracking=0.05, inside=False):
    """place glyphs along a circle; top arc reads left-to-right clockwise; bottom (inside=True) reads left-to-right counterclockwise."""
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm; sc = size / upm
    advs = [(gs[cmap[ord(c)]].width if ord(c) in cmap else upm * 0.3) * sc + tracking * size for c in s]
    total = sum(advs) - tracking * size
    ang_total = total / r
    out = ''
    a = math.radians(start_deg) - (ang_total / 2 if not inside else -ang_total / 2)
    for c, adv in zip(s, advs):
        g = cmap.get(ord(c))
        mid = a + (adv / 2 / r) * (1 if not inside else -1)
        if g and c != ' ':
            pen = SVGPathPen(gs)
            gw = gs[g].width * sc
            # place glyph centered at angle mid
            px = cx + r * math.sin(mid); py = cy - r * math.cos(mid)
            rot = math.degrees(mid) if not inside else math.degrees(mid) + 180
            ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            # glyph local: x from -gw/2.., baseline at 0 (y up in font units)
            ox = -gw / 2
            # transform: local (u,v) font -> scale -> rotate -> translate
            tp = TransformPen(pen, (sc * ca, sc * sa, sc * sa, -sc * ca, px + ox * ca, py + ox * sa))
            gs[g].draw(tp)
            out += pen.getCommands() + ' '
        a += (adv / r) * (1 if not inside else -1)
    return out

def concept_c(ink=INK, accent=BLUE, bg=None):
    W = H = 800; cx = cy = 400; R = 360
    body = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{ink}"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{R-78}" fill="{PAPER}"/>'
    body += f'<clipPath id="cc"><circle cx="{cx}" cy="{cy}" r="{R-78}"/></clipPath><g clip-path="url(#cc)">'
    shades = ['#e2cfa5', '#d4b680', '#c49d5f', '#a87f45', '#7d5c31']
    for i, col in enumerate(shades):
        rw = 640; x0 = cx - rw / 2
        base = cy + 160 + i * 0
        pts = ridge_pts(x0 - 10 + i * 6, cy + 30 + i * 44, rw, 120 - i * 14)
        poly = smooth_path(pts) + f' L{x0+rw:.0f},{cy+R} L{x0:.0f},{cy+R} Z'
        body += f'<path d="{poly}" fill="{col}"/>'
        if i == 0:
            body += f'<path d="{tower(pts, x0 - 10, rw, 34)}" fill="{shades[0]}"/>'
            top_pts = pts
    body += cliff_band(top_pts, cx - 330, 640, cy + 30, '#ffffff', sw=4, op=0.9)
    body += '</g>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{R-78}" fill="none" stroke="{ink}" stroke-width="6"/>'
    top = arc_text('HUDSON VALLEY CNC', bsd(800), 62, cx, cy, R - 58, 0, tracking=0.1)
    bot = arc_text('NEW PALTZ · NY', mono, 30, cx, cy, R - 30, 180, tracking=0.25, inside=True)
    body += f'<path d="{top}" fill="{PAPER}"/><path d="{bot}" fill="{TAN}"/>'
    for ang in (-62, 62):
        a = math.radians(ang + 180); px = cx + (R - 39) * math.sin(a); py = cy - (R - 39) * math.cos(a)
        body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{TAN}"/>'
    return svg(W, H, body, bg)

# ---------- D: Square icon / monogram
def concept_d(bg=None):
    W = H = 600
    body = f'<rect width="600" height="600" rx="64" fill="{INK}"/>'
    rw = 500; x0 = 50
    rw = 600; x0 = 0
    pts = ridge_pts(x0, 480, rw, 95)
    poly = smooth_path(pts) + f' L{x0+rw},600 L{x0},600 Z'
    body += f'<clipPath id="dc"><rect width="600" height="600" rx="64"/></clipPath><g clip-path="url(#dc)">'
    body += f'<path d="{poly}" fill="{BLUE}"/><path d="{tower(pts, x0, rw, 30)}" fill="{BLUE}"/>'
    body += f'<rect x="0" y="476" width="600" height="130" fill="{BLUE}"/>' + cliff_band(pts, x0, rw, 480, PAPER, sw=4, op=0.55) + '</g>'
    d1, _ = text_path('HV', bsd(800), 300, 300, 300, tracking=0.0, anchor='middle')
    d2, _ = text_path('CNC', mono, 64, 300, 548, tracking=0.35, anchor='middle')
    body += f'<path d="{d1}" fill="{PAPER}"/><path d="{d2}" fill="{PAPER}"/>'
    return svg(W, H, body, bg)

if __name__ == '__main__':
    O = '/home/claude/logo/out/'
    open(O + 'A-ridgeline.svg', 'w').write(concept_a())
    open(O + 'A-ridgeline-reverse.svg', 'w').write(concept_a(ink=PAPER, accent=TAN, bg=INK))
    open(O + 'B-toolpath.svg', 'w').write(concept_b())
    open(O + 'B-toolpath-reverse.svg', 'w').write(concept_b(ink=PAPER, accent='#5b8de0', bg=INK))
    open(O + 'C-badge.svg', 'w').write(concept_c())
    open(O + 'D-icon.svg', 'w').write(concept_d())
    print('ok')
