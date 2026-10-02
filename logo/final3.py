import sys; sys.path.insert(0, '/home/claude/logo')
from build3 import *
import build as B
import cairosvg, shutil, os
from shapely.geometry import Polygon, Point
O = '/home/claude/logo/final/'
shutil.rmtree(O, ignore_errors=True); os.makedirs(O + 'png'); os.makedirs(O + 'cnc')

def write(n, s): open(O + n, 'w').write(s)

def cliffs_svg(pts, x0, w, depth, col):
    cf, _ = cliff_face(pts, x0, w, depth, col)
    return f'<path d="{cf}" fill="{col}"/><path d="{left_cliffs(pts, x0, w, depth)}" fill="{col}"/>'

# lockups
write('logo-ridgeline.svg', concept_a3())
write('logo-ridgeline-reverse.svg', concept_a3(ink=PAPER, accent=TAN, cliff='#8f969a', sub_op=0.85))
write('logo-ridgeline-black.svg', concept_a3(ink='#000000', accent='#000000', cliff='#ffffff', sub_op=1))

# mark only
def mark(ink=INK, cliff=PAPER, bar=BLUE, W=1000, pad=40, rh=170):
    x0 = pad; w = W - 2 * pad; base = 300
    pts = ridge_pts(x0, base, w, rh)
    poly = smooth_path(pts) + f' L{x0+w:.2f},{base} L{x0:.2f},{base} Z'
    body = f'<path d="{poly}" fill="{ink}"/><path d="{tower_t(pts, x0, w, 54)}" fill="{ink}"/>' + cliffs_svg(pts, x0, w, rh * 0.42, cliff)
    body += f'<rect x="{x0}" y="{base}" width="{w}" height="12" fill="{bar}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 {W} 260" width="{W}" height="260">{body}</svg>'
write('mark-ridge.svg', mark())
write('mark-ridge-reverse.svg', mark(ink=PAPER, cliff='#8f969a', bar=TAN))
write('badge.svg', concept_c3())

def favicon():
    x0 = 30; w = 452; base = 330; rh = 100
    pts = ridge_pts(x0, base, w, rh)
    poly = smooth_path(pts) + f' L{x0+w:.2f},{base} L{x0:.2f},{base} Z'
    body = f'<rect width="512" height="512" rx="96" fill="{INK}"/>'
    body += f'<path d="{poly}" fill="{PAPER}"/><path d="{tower_t(pts, x0, w, 74)}" fill="{PAPER}"/>' + cliffs_svg(pts, x0, w, rh * 0.42, '#8f969a')
    body += f'<rect x="{x0}" y="{base}" width="{w}" height="22" fill="{TAN}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{body}</svg>'
write('favicon.svg', favicon())

for n, wpx in [('logo-ridgeline', 2400), ('logo-ridgeline-reverse', 2400), ('logo-ridgeline-black', 2400), ('mark-ridge', 2000),
               ('mark-ridge-reverse', 2000), ('badge', 2000), ('favicon', 512)]:
    cairosvg.svg2png(url=O + n + '.svg', write_to=O + 'png/' + n + '.png', output_width=wpx)
for px in (32, 180):
    cairosvg.svg2png(url=O + 'favicon.svg', write_to=O + f'png/favicon-{px}.png', output_width=px)

# ---- CNC geometry-only vectors
def cr_sample(pts, n=16):
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

import re
def path_pts(d):
    nums = list(map(float, re.findall(r'-?\d+\.?\d*', d)))
    return list(zip(nums[0::2], nums[1::2]))

def tower_poly(pts, x0, w, s):
    return Polygon(path_pts(tower_t(pts, x0, w, s)))

def P(points, close=True):
    return 'M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in points) + (' Z' if close else '')

def cliff_polys(pts, x0, w, depth):
    cf, _ = cliff_face(pts, x0, w, depth, '#fff')
    out = [Polygon(path_pts(cf))]
    for a, b, k in LEFT_CLIFFS:
        out.append(Polygon(path_pts(cliff_strip(pts, x0, w, a, b, depth * k))))
    return out

# ridge mark 12" wide (1 unit = 0.01")
x0 = 0; w = 1200; base = 300; rh = 204
pts = ridge_pts(x0, base, w, rh)
ridge = Polygon(cr_sample(pts) + [(x0 + w, base), (x0, base)]).buffer(0).union(tower_poly(pts, x0, w, 65))
paths = [P(list(ridge.exterior.coords))] + [P(list(c.exterior.coords)) for c in cliff_polys(pts, x0, w, rh * 0.42)]
minx, miny, maxx, maxy = ridge.bounds
write('cnc/cnc-ridge-mark-12in.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx-10:.1f} {miny-10:.1f} {maxx-minx+20:.1f} {maxy-miny+20:.1f}" width="{(maxx-minx+20)/100:.3f}in" height="{(maxy-miny+20)/100:.3f}in">'
      + ''.join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="1"/>' for d in paths) + '</svg>')

# badge geometry 18" (matches concept_c3 layout)
cx = cy = 400; R = 360; rw = 640
inner = Point(cx, cy).buffer(R - 78, resolution=256)
paths = [P(list(Point(cx, cy).buffer(R, resolution=256).exterior.coords)), P(list(inner.exterior.coords))]
for i in range(5):
    xx = cx - rw / 2 - 10 + i * 6
    lp = ridge_pts(xx, cy + 40 + i * 44, rw, 105 - i * 12)
    poly = Polygon(cr_sample(lp) + [(xx + rw, cy + R), (xx, cy + R)]).buffer(0)
    if i == 0:
        poly = poly.union(tower_poly(lp, xx, rw, 34))
        cl = cliff_polys(lp, xx, rw, 120 * 0.42)
    poly = poly.intersection(inner)
    for g in getattr(poly, 'geoms', [poly]): paths.append(P(list(g.exterior.coords)))
for c in cl:
    c = c.intersection(inner)
    for g in getattr(c, 'geoms', [c]): paths.append(P(list(g.exterior.coords)))
write('cnc/cnc-badge-geometry-18in.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 40 720 720" width="18in" height="18in">'
      + ''.join(f'<path d="{d}" fill="none" stroke="#000" stroke-width="1"/>' for d in paths) + '</svg>')

# header inline mark for the website (viewBox 0 4 120 38)
hx = 0; hw = 120; hb = 40; hrh = 24
hp = ridge_pts(hx, hb, hw, hrh)
hpoly = smooth_path(hp) + f' L{hx+hw},{hb} L{hx},{hb} Z'
cf, _ = cliff_face(hp, hx, hw, hrh * 0.42, 'x')
lc = left_cliffs(hp, hx, hw, hrh * 0.42)
svg_h = (f'<svg class="brand-mark" viewBox="0 6 120 35" aria-hidden="true" focusable="false">'
         f'<path d="{hpoly}" fill="currentColor"/><path d="{tower_t(hp, hx, hw, 10)}" fill="currentColor"/>'
         f'<path d="{cf} {lc}" style="fill:var(--paper)"/></svg>')
open('/home/claude/site/assets/brand-mark.svgfrag', 'w').write(svg_h)
print('done')
