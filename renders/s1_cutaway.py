import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
studio()
ply = wood('ply', scale=(1, 6, 1), ring=3); stud = wood('stud', (0.86, 0.72, 0.52), (0.72, 0.56, 0.36), (1, 1, 14), 4)
dry = mat('drywall', (0.86, 0.86, 0.84), 0.9)
ins = mat('ins', (0.92, 0.78, 0.30), 0.95, bump=(40, 0.6), noise=(30, 0.25))
wrap = mat('wrap', (0.93, 0.94, 0.95), 0.6, bump=(60, 0.15))
osbm = osb()
side = mat('siding', (0.10, 0.17, 0.22), 0.45)
trim = mat('trim', (0.93, 0.93, 0.91), 0.4)
char = mat('char', PALETTE['charcoal'], 0.5); wht = mat('wht', (0.95, 0.95, 0.95), 0.4)
acc = mat('acc', PALETTE['blue'], 0.4)

# plinth
box('plinth', (1.4, 0.55, 0.14), (0, 0, 0.07), ply, 0.004)
box('label', (0.6, 0.004, 0.07), (-0.2, -0.277, 0.07), char)
text('WALL SYSTEM CUTAWAY', (-0.2, -0.28, 0.07), 0.028, wht)
z0 = 0.14; H = 1.3; X0, X1 = -0.55, 0.55
# plates
box('bplate', (X1 - X0, 0.089, 0.038), (0, 0, z0 + 0.019), stud)
box('tplate', (X1 - X0, 0.089, 0.038), (0, 0, z0 + H - 0.019), stud)
box('tplate2', (X1 - X0, 0.089, 0.038), (0, 0, z0 + H + 0.019), stud)
xs = [X0 + 0.019, -0.13, 0.27, X1 - 0.019]
for i, x in enumerate(xs):
    box(f'stud{i}', (0.038, 0.089, H - 0.076), (x, 0, z0 + H / 2), stud)
for a, b in zip(xs[:-1], xs[1:]):
    w = b - a - 0.04
    o = box('ins', (w, 0.085, H - 0.08), ((a + b) / 2, 0, z0 + H / 2), ins, 0.01)
# drywall interior (back)
box('dry', (X1 - X0, 0.0127, H + 0.04), (0, 0.051, z0 + (H + 0.04) / 2), dry, 0.001)
# sheathing - cut back from left
sx0 = -0.30
box('osb', (X1 - sx0, 0.011, H + 0.04), ((X1 + sx0) / 2, -0.0505, z0 + (H + 0.04) / 2), osbm, 0.001)
# housewrap
wx0 = -0.12
box('wrap', (X1 - wx0, 0.0015, H + 0.04), ((X1 + wx0) / 2, -0.0570, z0 + (H + 0.04) / 2), wrap, 0)
# printed lines on wrap
for k in range(4):
    box('wline', (X1 - wx0, 0.0005, 0.006), ((X1 + wx0) / 2, -0.0580, z0 + 0.3 + k * 0.3), acc, 0)
# furring strips
for x in (0.0, 0.27, X1 - 0.02):
    box('fur', (0.04, 0.019, H + 0.04), (x, -0.068, z0 + (H + 0.04) / 2), stud)
# lap siding from x=0.08
sx = 0.08; bh = 0.15; n = int((H + 0.04) / (bh - 0.025)) + 1
for k in range(n):
    zc = z0 + 0.06 + k * (bh - 0.025)
    if zc > z0 + H: break
    o = box(f'sid{k}', (X1 - sx + 0.02, 0.014, bh), ((X1 + sx) / 2 + 0.01, -0.085, zc), side, 0.002, rot=(math.radians(-3), 0, 0))
# corner trim
box('ctrim', (0.06, 0.03, H + 0.06), (X1 + 0.03, -0.085, z0 + (H + 0.06) / 2), trim)
# callout tags
tags = [(-0.42, 'STUDS + INSULATION'), (-0.21, 'SHEATHING'), (-0.02, 'WRB'), (0.32, 'SIDING')]
for i, (x, t) in enumerate(tags):
    zz = z0 + 1.0 - i * 0.18
    box(f'tag{i}', (0.22, 0.004, 0.055), (x, -0.13 - i * 0.012, zz), acc, 0.002)
    text(t, (x, -0.133 - i * 0.012, zz), 0.019, wht)

light((-2.5, -2.5, 3.0), 900, 3)
light((2.5, -1.5, 2.0), 350, 2)
light((0, 2, 3), 200, 3)
camera((-2.35, -1.45, 1.25), (0.05, 0, 0.72), lens=45, dof=8)
render('/home/claude/renders/out/cutaway-wall.jpg')
