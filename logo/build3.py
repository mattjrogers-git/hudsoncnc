import sys; sys.path.insert(0, '/home/claude/logo'); sys.path.insert(0, '/home/claude/logo/photo')
import build as B
from build import *
from profile import RIDGE_PHOTO, TOWER_X_PHOTO, CLIFF_PHOTO
B.RIDGE[:] = RIDGE_PHOTO
B.TOWER_X = TOWER_X_PHOTO
import importlib

def ridge_y(pts, x): return ridge_y_at(pts, x)

def cliff_face(pts, x0, w, depth, col):
    a = x0 + (CLIFF_PHOTO[0] + 3) / 1000 * w; b = x0 + CLIFF_PHOTO[1] / 1000 * w
    top = []; x = a
    while x <= b:
        top.append((x, ridge_y(pts, x) + depth * 0.05)); x += (b - a) / 60
    bot = []
    for x, y in reversed(top):
        f = (x - a) / (b - a)
        bot.append((x, ridge_y(pts, x) + depth * (1 - f) ** 1.1 + depth * 0.05))
    d = 'M' + ' L'.join(f'{p[0]:.2f},{p[1]:.2f}' for p in top + bot) + ' Z'
    # a few vertical cracks
    cr = ''
    for i in range(1, 7):
        f = i / 8; x = a + (b - a) * f
        y = ridge_y(pts, x) + depth * 0.15; L = depth * (1 - f) ** 0.8 * 0.7
        pass
    return d, cr

def tower_t(pts, x0, w, s):
    # tower sits on crest at TOWER_X
    tx = x0 + B.TOWER_X / 1000 * w; ty = ridge_y(pts, tx) + s * 0.1; tw = s * 0.42
    return (f'M{tx - tw/2:.2f},{ty:.2f} L{tx - tw/2:.2f},{ty - s*0.82:.2f} L{tx - tw*0.62:.2f},{ty - s*0.82:.2f} L{tx - tw*0.62:.2f},{ty - s:.2f} '
            f'L{tx + tw*0.62:.2f},{ty - s:.2f} L{tx + tw*0.62:.2f},{ty - s*0.82:.2f} L{tx + tw/2:.2f},{ty - s*0.82:.2f} L{tx + tw/2:.2f},{ty:.2f} Z')

def concept_a3(ink=INK, accent=BLUE, bg=None, cliff=PAPER, sub_op=0.8, rh=120):
    W, H = 1000, 560
    d1, w1 = text_path('HUDSON VALLEY CNC', bsd(800), 150, 0, 0, tracking=0.01)
    sc = 860 / w1; x0 = (W - 860) / 2
    pts = ridge_pts(x0, 300, 860, rh)
    poly = smooth_path(pts) + f' L{x0+860:.2f},300 L{x0:.2f},300 Z'
    body = f'<path d="{poly}" fill="{ink}"/><path d="{tower_t(pts, x0, 860, 40)}" fill="{ink}"/>'
    cf, cr = cliff_face(pts, x0, 860, rh * 0.42, cliff)
    body += f'<path d="{cf}" fill="{cliff}"/><path d="{cr}" stroke="{ink}" stroke-width="2.2" stroke-linecap="round" opacity="0.7"/>'
    body += f'<rect x="{x0}" y="300" width="860" height="10" fill="{accent}"/>'
    dA, _ = text_path('HUDSON VALLEY CNC', bsd(800), 150 * sc, x0, 300 + 30 + cap_height(bsd(800), 150 * sc), tracking=0.01)
    body += f'<path d="{dA}" fill="{ink}"/>'
    dB, _ = text_path('CNC ROUTING  ·  FABRICATION  ·  NEW PALTZ, NY', mono, 26, W / 2, 520, tracking=0.12, anchor='middle')
    body += f'<path d="{dB}" fill="{ink}" opacity="{sub_op}"/>'
    return svg(W, H, body, bg)

def concept_c3():
    W = H = 800; cx = cy = 400; R = 360
    body = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="{R-78}" fill="{PAPER}"/>'
    body += f'<clipPath id="cc"><circle cx="{cx}" cy="{cy}" r="{R-78}"/></clipPath><g clip-path="url(#cc)">'
    shades = ['#e2cfa5', '#d4b680', '#c49d5f', '#a87f45', '#7d5c31']
    rw = 640
    for i, col in enumerate(shades):
        x0 = cx - rw / 2 - 10 + i * 6
        pts = ridge_pts(x0, cy + 40 + i * 44, rw, 105 - i * 12)
        poly = smooth_path(pts) + f' L{x0+rw:.0f},{cy+R} L{x0:.0f},{cy+R} Z'
        body += f'<path d="{poly}" fill="{col}"/>'
        if i == 0:
            body += f'<path d="{tower_t(pts, x0, rw, 34)}" fill="{col}"/>'
            cf, cr = cliff_face(pts, x0, rw, (120) * 0.42, '#ffffff')
            top = (cf, cr)
    body += f'<path d="{top[0]}" fill="#f7f3ea"/><path d="{top[1]}" stroke="#c9a46c" stroke-width="2" stroke-linecap="round"/>'
    body += '</g>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{R-78}" fill="none" stroke="{INK}" stroke-width="6"/>'
    top_t = arc_text('HUDSON VALLEY CNC', bsd(800), 62, cx, cy, R - 58, 0, tracking=0.1)
    bot = arc_text('NEW PALTZ · NY', mono, 30, cx, cy, R - 30, 180, tracking=0.25, inside=True)
    body += f'<path d="{top_t}" fill="{PAPER}"/><path d="{bot}" fill="{TAN}"/>'
    for ang in (-62, 62):
        a = math.radians(ang + 180); px = cx + (R - 39) * math.sin(a); py = cy - (R - 39) * math.cos(a)
        body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{TAN}"/>'
    return svg(W, H, body)

if __name__ == '__main__':
    O = '/home/claude/logo/out/'
    open(O + 'A3-ridgeline.svg', 'w').write(concept_a3())
    open(O + 'A3-ridgeline-reverse.svg', 'w').write(concept_a3(ink=PAPER, accent=TAN, bg=INK, cliff='#8f969a', sub_op=0.85))
    open(O + 'C3-badge.svg', 'w').write(concept_c3())
    print('ok')
