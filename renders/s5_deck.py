import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
studio()
ply = wood('ply', scale=(1, 6, 1), ring=3)
char = mat('char', PALETTE['charcoal'], 0.45); blue = mat('blue', PALETTE['blue'], 0.35)
white = mat('white', (0.92, 0.92, 0.9), 0.35)
cols = [(0.40, 0.25, 0.15), (0.30, 0.29, 0.28), (0.52, 0.38, 0.26), (0.20, 0.16, 0.13), (0.55, 0.53, 0.50), (0.42, 0.30, 0.22)]
boards = [wood(f'dk{i}', c, tuple(v * 0.75 for v in c), (1, 20, 1), 5) for i, c in enumerate(cols)]
# slanted display rack: build in a local frame, then tilt back
import bpy
bpy.ops.object.empty_add(location=(0, 0.15, 0.25)); piv = bpy.context.object
parts = []
H = 1.25
parts.append(box('rackback', (1.16, 0.03, H), (0, 0.15 + 0.03, 0.25 + H / 2), ply, 0.004))
for sx in (-0.6, 0.6):
    parts.append(box('rail', (0.04, 0.05, H + 0.05), (sx, 0.15, 0.25 + H / 2), char, 0.003))
for i, m in enumerate(boards):
    z = 0.25 + 0.1 + i * 0.19
    parts.append(box(f'board{i}', (1.12, 0.03, 0.15), (0, 0.15 - 0.02, z), m, 0.006))
    parts.append(box(f'tag{i}', (0.15, 0.004, 0.035), (0.44, 0.15 - 0.037, z), white, 0.001))
parts.append(box('header', (1.24, 0.04, 0.22), (0, 0.15, 0.25 + H + 0.14), blue, 0.004))
parts.append(text('DECKING COLLECTION', (0, 0.15 - 0.022, 0.25 + H + 0.15), 0.07, white))
for o in parts:
    o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
piv.rotation_euler = (math.radians(-14), 0, 0)
# legs / base
box('base', (1.3, 0.55, 0.06), (0, 0.25, 0.03), char, 0.004)
for sx in (-0.6, 0.6):
    box('strut', (0.04, 0.04, 0.5), (sx, 0.38, 0.25), char, 0.003, rot=(math.radians(-14), 0, 0))
light((-2, -2.6, 2.8), 950, 2.5); light((2.3, -1.6, 2.4), 330, 2); light((0, 2.5, 3), 200, 3)
camera((-1.6, -2.9, 1.3), (0, 0.2, 0.95), lens=40, dof=7)
render('/home/claude/renders/out/decking-sample-display.jpg')
