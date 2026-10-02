import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
# usage: python3 s7_bison.py <scene: small|paver> <samples>
scene = sys.argv[-2]
reset(samples=int(sys.argv[-1]))
random.seed(4)
studio()
blk = mat('pedblk', (0.025, 0.025, 0.028), 0.55, bump=(400, 0.05))
yel = mat('yel', (0.85, 0.62, 0.05), 0.4)
pvc = mat('pvc', (0.92, 0.92, 0.91), 0.35)
pt = wood('pt', (0.80, 0.70, 0.48), (0.66, 0.55, 0.34), (1, 1, 16), 4)
steel = mat('steel', (0.6, 0.62, 0.64), 0.35, metal=1.0)
grav = mat('grav', (0.55, 0.52, 0.48), 0.9, bump=(90, 0.9), noise=(60, 0.35))


def pedestal(x, y, z, h=0.16, s=1.0):
    """generic adjustable deck pedestal: square footing pad, cone, threaded column, lock ring, head."""
    box('pad', (0.22 * s, 0.22 * s, 0.012 * s), (x, y, z + 0.006 * s), blk, 0.01)
    cone('cone', 0.10 * s, 0.05 * s, 0.05 * s, (x, y, z + 0.037 * s), blk)
    col_h = h - 0.10 * s
    cyl('col', 0.036 * s, col_h, (x, y, z + 0.062 * s + col_h / 2), blk)
    n = int(col_h / (0.006 * s))
    for i in range(n):
        cyl('thr', 0.039 * s, 0.002 * s, (x, y, z + 0.064 * s + i * 0.006 * s), blk, verts=32)
    cyl('ring', 0.045 * s, 0.014 * s, (x, y, z + 0.062 * s + col_h * 0.55), yel)
    top = z + 0.062 * s + col_h
    cyl('neck', 0.03 * s, 0.02 * s, (x, y, top + 0.01 * s), blk)
    cyl('head', 0.065 * s, 0.012 * s, (x, y, top + 0.026 * s), blk)
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        box('tab', (0.012 * s, 0.05 * s, 0.03 * s), (x + math.cos(ang) * 0.03 * s, y + math.sin(ang) * 0.03 * s, top + 0.045 * s), blk, 0.001, rot=(0, 0, ang))
    return top + 0.06 * s


if scene == 'small':
    # three-sided PVC in-store display with pedestal and a 2x6 joist
    W, D, H, T = 0.40, 0.34, 0.36, 0.019
    box('base', (W, D, T), (0, 0, T / 2), pvc, 0.002)
    box('back', (W - 2 * T - 0.001, T, H), (0, D / 2 - T / 2, H / 2 + T), pvc, 0.002)
    for sx in (-1, 1):
        box('side', (T, D - 0.004, H), (sx * (W / 2 - T / 2), 0.002, H / 2 + T + 0.0005), pvc, 0.0015)
    # gravel patch
    for i in range(260):
        r = random.uniform(0.004, 0.009)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=(random.uniform(-0.17, 0.17), random.uniform(-0.15, 0.14), T + r * 0.6))
        o = bpy.context.object; o.scale = (1, random.uniform(0.6, 1.2), 0.6); o.data.materials.append(grav)
    top = pedestal(0, 0.0, T, h=0.17)
    # 2x6 joist spanning side to side, resting in head
    box('joist', (W - 2 * T, 0.038, 0.14), (0, 0, top + 0.07), pt, 0.003)
    for sx in (-1, 1):
        box('clip', (0.003, 0.05, 0.06), (sx * (W / 2 - T - 0.0015), -0.03, top + 0.07), steel, 0.0005)
    box('lblstrip', (0.24, 0.002, 0.016), (0, -D / 2 - 0.0005, T / 2), mat('lw', (0.95,0.95,0.95), 0.4), 0)
    text('ADJUSTABLE PEDESTAL', (0, -D / 2 - 0.0026, T / 2), 0.016, mat('lbl', (0.1, 0.25, 0.6), 0.4), rot=(math.radians(90), 0, 0))
    light((-1.2, -1.4, 1.5), 260, 1.4); light((1.2, -0.8, 1.0), 90, 1); light((0, 1.0, 1.4), 70, 1.5)
    camera((-0.62, -0.95, 0.62), (0, 0.02, 0.2), lens=50, dof=4)
    render('/home/claude/renders/out/bison-small-display.jpg')
else:
    # row of paver pedestal demo pieces
    pav = mat('paver', (0.62, 0.61, 0.58), 0.45, bump=(25, 0.15), noise=(8, 0.25))
    galv = mat('galv', (0.7, 0.72, 0.73), 0.45, metal=0.8, noise=(40, 0.2))
    table = mat('tbl2', (0.5, 0.36, 0.24), 0.5)
    for i, x in enumerate((-0.32, 0.0, 0.32)):
        top = pedestal(x, 0.0 + i * 0.02, 0, h=0.12 + i * 0.02, s=0.9)
        box('backer', (0.078, 0.30, 0.003), (x, i * 0.02, top + 0.0015), galv, 0.0005)
        box('paverstrip', (0.076, 0.30, 0.02), (x, i * 0.02, top + 0.013), pav, 0.0015)
    light((-1.2, -1.5, 1.6), 300, 1.6); light((1.4, -0.8, 1.1), 110, 1.2); light((0, 1.2, 1.5), 80, 1.5)
    camera((-0.55, -1.15, 0.55), (0, 0.02, 0.1), lens=50, dof=4)
    render('/home/claude/renders/out/bison-paver-demos.jpg')
