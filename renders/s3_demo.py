import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
studio()
ply = wood('ply', scale=(1, 6, 1), ring=3); oak = wood('oak', (0.62, 0.45, 0.27), (0.45, 0.30, 0.16), (1, 10, 1), 4)
char = mat('char', PALETTE['charcoal'], 0.45); blue = mat('blue', PALETTE['blue'], 0.35)
white = mat('white', (0.9, 0.9, 0.88), 0.35); orange = mat('or', PALETTE['orange'], 0.35)
tile = mat('tile', (0.93, 0.93, 0.92), 0.15); grout = mat('grout', (0.55, 0.55, 0.53), 0.8)
dry = mat('dry', (0.85, 0.85, 0.83), 0.9); bead = mat('bead', (0.96, 0.96, 0.95), 0.25)
gbead = mat('gbead', (0.4, 0.41, 0.42), 0.3)
# table
box('top', (1.4, 0.7, 0.04), (0, 0, 0.9), ply, 0.004)
for x in (-0.66, 0.66):
    for y in (-0.31, 0.31):
        box('leg', (0.05, 0.05, 0.88), (x, y, 0.44), char, 0.003)
box('apron', (1.36, 0.02, 0.12), (0, -0.33, 0.82), blue, 0.002)
text('HANDS-ON DEMO', (0, -0.342, 0.82), 0.05, white)
# test board frame: three substrates angled
Z = 0.92
box('frameb', (1.05, 0.30, 0.03), (0, 0.05, Z + 0.015), ply)
subs = [('WOOD', oak), ('TILE', tile), ('DRYWALL', dry)]
for i, (lbl, m) in enumerate(subs):
    x = -0.34 + i * 0.34
    o = box(f'sub{i}', (0.30, 0.02, 0.38), (x, 0.12, Z + 0.21), m, 0.002, rot=(math.radians(-12), 0, 0))
    if lbl == 'TILE':
        for g in range(1, 4):
            box('g', (0.30, 0.004, 0.006), (x, 0.108 + g * 0.0, Z + 0.03 + g * 0.095), grout, 0, rot=(math.radians(-12), 0, 0))
        box('gv', (0.006, 0.004, 0.38), (x, 0.108, Z + 0.21), grout, 0, rot=(math.radians(-12), 0, 0))
    for b in range(3):
        zb = Z + 0.10 + b * 0.11
        yb = 0.12 - 0.012 - (zb - Z - 0.21) * math.tan(math.radians(12))
        cyl('bead', 0.006, 0.24, (x, yb, zb), bead if b % 2 == 0 else gbead, rot=(0, math.radians(90), 0))
    box('lab', (0.2, 0.004, 0.04), (x, -0.04, Z + 0.035), char, 0.001)
    text(lbl, (x, -0.0425, Z + 0.035), 0.022, white)
# tubes on table
for k, bm in enumerate([blue, orange, blue, orange]):
    tube((0.52 + (k % 2) * 0.07, -0.18 + (k // 2) * 0.08, Z), white, bm, white, name=f'tt{k}')
# backer sign
box('backer', (1.3, 0.02, 0.9), (0, 0.36, 1.37), ply, 0.003)
box('panel', (1.1, 0.01, 0.22), (0, 0.345, 1.63), blue, 0.003)
text('SEE IT WORK', (0, 0.338, 1.65), 0.075, white)
text('Try every product on real job-site materials', (0, 0.338, 1.575), 0.028, white)
light((-2, -2.4, 2.8), 950, 2.5); light((2.2, -1.5, 2.2), 330, 2); light((0, 2.5, 3), 200, 3)
camera((-1.2, -2.25, 1.75), (0, 0.05, 1.1), lens=42, dof=6)
render('/home/claude/renders/out/hands-on-demo-station.jpg')
