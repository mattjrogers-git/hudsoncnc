import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
studio()
ply = wood('ply', scale=(1, 6, 1), ring=3)
blue = mat('blue', PALETTE['blue'], 0.35); orange = mat('or', PALETTE['orange'], 0.35)
white = mat('white', (0.9, 0.9, 0.88), 0.35); char = mat('char', PALETTE['charcoal'], 0.45)
grey = mat('grey', (0.55, 0.57, 0.6), 0.4)
counter = mat('counter', (0.18, 0.19, 0.2), 0.3)
# store counter top
box('counter', (2.2, 0.9, 0.04), (0, 0.1, 0.9), counter, 0.004)
box('counterbody', (2.2, 0.85, 0.88), (0, 0.12, 0.44), mat('cb', (0.75, 0.75, 0.74), 0.6))
Z = 0.92
W, D = 0.62, 0.40
# sides (stepped profile via three stacked blocks)
for sx in (-W / 2, W / 2):
    for i in range(3):
        box('side', (0.018, D - i * 0.12, 0.10 + i * 0.09), (sx, 0.0 + i * 0.06, Z + (0.10 + i * 0.09) / 2), ply, 0.002)
# steps
for i in range(3):
    zt = Z + 0.10 + i * 0.09
    box(f'step{i}', (W - 0.018, 0.12, 0.018), (0, -D / 2 + 0.06 + i * 0.12, zt - 0.009), ply, 0.002)
    box(f'riser{i}', (W - 0.018, 0.012, 0.10 + i * 0.09), (0, -D / 2 + i * 0.12 + 0.006, Z + (0.10 + i * 0.09) / 2), white, 0.001)
    bands = [blue, orange, grey]
    for k in range(5):
        x = -W / 2 + 0.07 + k * 0.12
        tube((x, -D / 2 + 0.06 + i * 0.12, zt), white, bands[i], white, name=f't{i}{k}')
# back + header
box('back', (W, 0.018, 0.55), (0, D / 2 - 0.02, Z + 0.275), ply, 0.002)
box('header', (W + 0.04, 0.02, 0.17), (0, D / 2 - 0.04, Z + 0.62), blue, 0.004)
text('YOUR BRAND', (0, D / 2 - 0.0515, Z + 0.645), 0.065, white)
text('PRO SEALANT SYSTEM', (0, D / 2 - 0.0515, Z + 0.582), 0.024, white)
box('base', (W + 0.02, D, 0.02), (0, 0, Z + 0.01), ply, 0.002)
# price strip
box('strip', (W, 0.004, 0.035), (0, -D / 2 - 0.004, Z + 0.035), char, 0.001)
text('NEW  •  PROFESSIONAL GRADE  •  NEW', (0, -D / 2 - 0.0065, Z + 0.035), 0.016, white)
light((-1.8, -2.2, 2.6), 900, 2.5); light((2, -1.2, 2.2), 300, 2); light((0, 2.5, 2.8), 250, 3)
camera((-1.15, -1.9, 1.6), (0, 0.02, 1.22), lens=50, dof=4)
render('/home/claude/renders/out/pop-counter-display.jpg')
