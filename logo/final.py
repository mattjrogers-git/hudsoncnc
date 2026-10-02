import sys; sys.path.insert(0, '/home/claude/logo')
from build import *
import cairosvg
from shapely.geometry import Polygon, Point
O = '/home/claude/logo/final/'

def cr_sample(pts, n=16):
    """sample the same Catmull-Rom curve smooth_path draws."""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        t = 0.18
        c1 = (p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t)
        c2 = (p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t)
        for k in range(1, n + 1):
            u = k / n; a = (1-u)**3; b = 3*(1-u)**2*u; c = 3*(1-u)*u**2; d = u**3
            out.append((a*p1[0]+b*c1[0]+c*c2[0]+d*p2[0], a*p1[1]+b*c1[1]+c*c2[1]+d*p2[1]))
    return out

def write(name, s):
    open(O + name, 'w').write(s)

# 1-3 ridgeline lockups (transparent)
write('logo-ridgeline.svg', concept_a())
write('logo-ridgeline-reverse.svg', concept_a(ink=PAPER, accent=TAN, cliff=INK, sub_op=0.85))
write('logo-ridgeline-black.svg', concept_a(ink='#000000', accent='#000000', cliff='#ffffff', sub_op=1))

# 4 mark only
def mark(ink=INK, cliff=PAPER, bar=BLUE, W=1000, pad=40):
    x0 = pad; w = W - 2 * pad; base = 300
    pts = ridge_pts(x0, base, w, 190)
    poly = smooth_path(pts) + f' L{x0+w:.2f},{base} L{x0:.2f},{base} Z'
    body = f'<path d="{poly}" fill="{ink}"/><path d="{tower(pts, x0, w, 56)}" fill="{ink}"/>'
    body += cliff_band(pts, x0, w, base, cliff, sw=6, op=1)
    body += f'<rect x="{x0}" y="{base}" width="{w}" height="12" fill="{bar}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 40 {W} 280" width="{W}" height="280">{body}</svg>'
write('mark-ridge.svg', mark())
write('mark-ridge-reverse.svg', mark(ink=PAPER, cliff=INK, bar=TAN))

# 5 badge
write('badge.svg', concept_c())

# 6 favicon: ridge on dark rounded square
def favicon():
    x0 = 36; w = 440; base = 366
    pts = ridge_pts(x0, base, w, 180)
    poly = smooth_path(pts) + f' L{x0+w:.2f},{base} L{x0:.2f},{base} Z'
    body = f'<rect width="512" height="512" rx="96" fill="{INK}"/>'
    body += f'<path d="{poly}" fill="{PAPER}"/><path d="{tower(pts, x0, w, 60)}" fill="{PAPER}"/>'
    body += cliff_band(pts, x0, w, base, INK, sw=10, op=1, off=16)
    body += f'<rect x="{x0}" y="{base}" width="{w}" height="22" fill="{TAN}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{body}</svg>'
write('favicon.svg', favicon())

# PNGs
for n, wpx in [('logo-ridgeline', 2400), ('logo-ridgeline-reverse', 2400), ('logo-ridgeline-black', 2400), ('mark-ridge', 2000),
               ('mark-ridge-reverse', 2000), ('badge', 2000), ('favicon', 512)]:
    cairosvg.svg2png(url=O + n + '.svg', write_to=O + 'png/' + n + '.png', output_width=wpx)
for px in (32, 180):
    cairosvg.svg2png(url=O + 'favicon.svg', write_to=O + f'png/favicon-{px}.png', output_width=px)

# 7 CNC geometry-only vectors (no text), outlines only, sized in inches
def P(points, close=True):
    d = 'M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in points)
    return d + (' Z' if close else '')

def tower_pts(pts, x0, w, s):
    tx = x0 + TOWER_X / 1000 * w; ty = ridge_y_at(pts, tx) + s * 0.08; tw = s * 0.42
    return [(tx - tw/2, ty), (tx - tw/2, ty - s*0.82), (tx - tw*0.62, ty - s*0.82), (tx - tw*0.62, ty - s), (tx + tw*0.62, ty - s),
            (tx + tw*0.62, ty - s*0.82), (tx + tw/2, ty - s*0.82), (tx + tw/2, ty)]

def cliff_lines(pts, x0, w, off):
    out = []
    for X0, X1 in ((225, 385), (410, 545), (590, 790)):
        seg = []; x = x0 + X0 / 1000 * w
        while x <= x0 + X1 / 1000 * w:
            seg.append((x, ridge_y_at(pts, x) + off)); x += 2
        out.append(seg)
    return out

# ridge mark, 12" wide; units: 1 unit = 0.01 in
x0 = 0; w = 1200; base = 300
pts = ridge_pts(x0, base, w, 228)
fine = cr_sample(pts)
ridge = Polygon(fine + [(x0 + w, base), (x0, base)]).union(Polygon(tower_pts(pts, x0, w, 67)))
paths = [P(list(ridge.exterior.coords))]
paths += [P(seg, close=False) for seg in cliff_lines(pts, x0, w, 26)]
minx, miny, maxx, maxy = ridge.bounds
vb = f'{minx-10:.1f} {miny-10:.1f} {maxx-minx+20:.1f} {maxy-miny+20:.1f}'
svgc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{(maxx-minx+20)/100:.3f}in" height="{(maxy-miny+20)/100:.3f}in">'
        + ''.join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="1"/>' for d in paths) + '</svg>')
write('cnc/cnc-ridge-mark-12in.svg', svgc)

# badge geometry, 18" diameter: outer ring, inner ring, clipped ridge layers, tower, cliff lines
cx = cy = 400; R = 360
inner = Point(cx, cy).buffer(R - 78, resolution=256)
paths = [P(list(Point(cx, cy).buffer(R, resolution=256).exterior.coords)), P(list(inner.exterior.coords))]
for i in range(5):
    rw = 640; xx = cx - rw / 2
    lp = ridge_pts(xx - 10 + i * 6, cy + 10 + i * 46, rw, 150 - i * 18)
    lp = ridge_pts(xx - 10 + i * 6, cy + 30 + i * 44, rw, 120 - i * 14)
    poly = Polygon(cr_sample(lp) + [(xx + rw, cy + R), (xx, cy + R)]).intersection(inner)
    if i == 0:
        poly = poly.union(Polygon(tower_pts(lp, xx - 10, rw, 34)))
        top_pts = lp
    geoms = getattr(poly, 'geoms', [poly])
    for g in geoms: paths.append(P(list(g.exterior.coords)))
for seg in cliff_lines(top_pts, cx - 330, 640, max(5, 120 * 0.11)):
    paths.append(P(seg, close=False))
sc = 18 / 720  # 720 units -> 18 in
svgb = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 40 720 720" width="18in" height="18in">'
        + ''.join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="1"/>' for d in paths) + '</svg>')
write('cnc/cnc-badge-geometry-18in.svg', svgb)

# header inline mark path (viewBox 0 0 120 44) for the website
hx = 0; hw = 120; hb = 40
hp = ridge_pts(hx, hb, hw, 26)
hpoly = smooth_path(hp) + f' L{hx+hw},{hb} L{hx},{hb} Z'
open(O + 'header-mark.txt', 'w').write(hpoly + '\n' + tower(hp, hx, hw, 9) + '\n' + cliff_band(hp, hx, hw, hb, 'X', sw=1.2, op=1, off=3.2))
print('done')
