import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
pass
# use a walnut tabletop instead of the plain floor
wal = wood('walnut', (0.36, 0.22, 0.13), (0.22, 0.13, 0.07), (1, 8, 1), 3)
box('table', (8, 6, 0.04), (0, 0, -0.025), mat('tbl', (0.45, 0.31, 0.2), 0.45), 0)
box('bgwall', (8, 0.02, 4), (0, 1.3, 2), mat('bgw', (0.72, 0.73, 0.75), 0.8), 0)
char = mat('char', (0.06, 0.065, 0.07), 0.35); foam = mat('foam', (0.16, 0.165, 0.17), 0.95, bump=(160, 0.25))
blue = mat('blue', PALETTE['blue'], 0.35); white = mat('white', (0.92, 0.92, 0.9), 0.35); orange = mat('or', PALETTE['orange'], 0.35)
birch = wood('birch', (0.85, 0.72, 0.52), (0.72, 0.58, 0.38), (1, 8, 1), 3)
oak = wood('oak', (0.62, 0.45, 0.27), (0.45, 0.30, 0.16), (1, 10, 1), 4)
pvc = mat('pvc', (0.93, 0.93, 0.92), 0.3); comp = mat('comp', (0.32, 0.27, 0.23), 0.6, bump=(80, 0.2))
W, D, Hb = 0.48, 0.34, 0.07
# base shell
box('shell', (W, D, Hb), (0, 0, Hb / 2), char, 0.008)
box('foam', (W - 0.02, D - 0.02, 0.012), (0, 0, Hb - 0.004), foam, 0.002)
# lid hinged at back, opened ~105 deg
import bpy
bpy.ops.object.empty_add(location=(0, D / 2, Hb)); piv = bpy.context.object
lid = box('lid', (W, D, 0.03), (0, D / 2 + D / 2, Hb + 0.015), char, 0.008)
lidin = box('lidin', (W - 0.04, D - 0.04, 0.004), (0, D, Hb + 0.032), blue, 0.002)
t1 = text('YOUR BRAND', (0, D + 0.03, Hb + 0.035), 0.05, white, rot=(0, 0, 0))
t2 = text('Sales Demo Kit', (0, D - 0.04, Hb + 0.035), 0.022, white, rot=(0, 0, 0))
for o in (lid, lidin, t1, t2):
    o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
piv.rotation_euler = (math.radians(100), 0, 0)
# items sitting in foam recesses (slightly sunk)
z = Hb + 0.002
items = [(-0.16, 0.07, birch), (-0.06, 0.07, oak), (0.04, 0.07, pvc), (0.14, 0.07, comp)]
for x, y, m in items:
    box('blk', (0.085, 0.085, 0.03), (x, y, z + 0.008), m, 0.003)
# simpler: lay small tubes as horizontal cylinders
for k, bm in enumerate([blue, orange, blue]):
    y = -0.04 - k * 0.045
    cyl(f'lt{k}', 0.016, 0.16, (0.0, y, z + 0.01), white, rot=(0, math.radians(90), 0))
    cyl(f'lb{k}', 0.0163, 0.08, (-0.01, y, z + 0.01), bm, rot=(0, math.radians(90), 0))
    cone(f'ln{k}', 0.008, 0.002, 0.05, (0.105, y, z + 0.01), white, rot=(0, math.radians(90), 0))
# swatch card
box('card', (0.11, 0.15, 0.003), (0.17, -0.08, z + 0.002), white, 0.001)
for i, m in enumerate([blue, orange, comp, oak]):
    box('sw', (0.08, 0.025, 0.002), (0.17, -0.025 - i * 0.033, z + 0.004), m, 0)
light((-1.2, -1.3, 1.8), 500, 1.5); light((1.2, -0.6, 1.2), 150, 1); light((0, -0.5, 2.2), 260, 2.5)
camera((-0.35, -0.95, 0.62), (0, 0.08, 0.16), lens=45, dof=5)
render('/home/claude/renders/out/sales-demo-kit.jpg')
