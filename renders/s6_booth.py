import sys; sys.path.insert(0, '/home/claude/renders')
from lib import *
reset(samples=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 96)
# hall floor + dark backdrop
fl = mat('hall', (0.45, 0.46, 0.47), 0.6)
bpy.ops.mesh.primitive_plane_add(size=40); bpy.context.object.data.materials.append(fl)
bk = mat('bk', (0.12, 0.13, 0.15), 0.9)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 6, 0), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(bk)
ply = wood('ply', scale=(1, 6, 1), ring=3); stud = wood('stud', (0.86, 0.72, 0.52), (0.72, 0.56, 0.36), (1, 1, 14), 4)
ins = mat('ins', (0.92, 0.78, 0.30), 0.95, bump=(40, 0.6)); osbm = osb(); wrap = mat('wrap', (0.93, 0.94, 0.95), 0.6)
side = mat('siding', (0.10, 0.17, 0.22), 0.45)
carpet = mat('carpet', (0.08, 0.12, 0.22), 0.95, bump=(300, 0.3))
char = mat('char', PALETTE['charcoal'], 0.45); blue = mat('blue', PALETTE['blue'], 0.35)
white = mat('white', (0.92, 0.92, 0.9), 0.35); orange = mat('or', PALETTE['orange'], 0.35)
# carpet 3x3
box('carpet', (3.05, 3.05, 0.01), (0, 0, 0.005), carpet, 0)
# back wall with vertical slats
box('wall', (3.0, 0.05, 2.4), (0, 1.5, 1.2), char, 0.003)
for i in range(30):
    x = -1.45 + i * 0.1
    box('slat', (0.06, 0.03, 2.3), (x, 1.46, 1.2), ply, 0.003)
# header band
box('hdr', (3.0, 0.06, 0.42), (0, 1.43, 2.6), blue, 0.004)
text('YOUR BRAND', (0, 1.395, 2.62), 0.2, white)
# shelves on wall
for j in range(3):
    z = 1.0 + j * 0.35
    box('shelf', (1.1, 0.25, 0.025), (0.8, 1.31, z), ply, 0.003)
    for k in range(9):
        tube((0.36 + k * 0.11, 1.31, z + 0.0125), white, blue if (k + j) % 2 else orange, white, name=f'sh{j}{k}')
# graphic panel left
box('gpanel', (0.9, 0.02, 1.2), (-0.85, 1.42, 1.5), white, 0.003)
text('BUILT TO', (-0.85, 1.405, 1.8), 0.11, char); text('LAST', (-0.85, 1.405, 1.62), 0.16, blue)
text('Live demos  •  Samples  •  New products', (-0.85, 1.405, 1.35), 0.04, char)
# cutaway wall model on left
mini_cutaway(-1.05, 0.55, 0.01, 0.95, (ply, stud, ins, osbm, wrap, side))
# demo counter front right
box('counter', (1.2, 0.55, 0.95), (0.75, -0.6, 0.485), ply, 0.004)
box('ctop', (1.25, 0.6, 0.03), (0.75, -0.6, 0.975), char, 0.003)
box('cface', (1.0, 0.01, 0.4), (0.75, -0.881, 0.6), blue, 0.002)
text('TRY IT', (0.75, -0.888, 0.62), 0.12, white)
for k in range(4):
    tube((0.4 + k * 0.12, -0.55, 0.99), white, orange if k % 2 else blue, white, name=f'ct{k}')
box('testbd', (0.4, 0.02, 0.3), (1.05, -0.5, 1.14), stud, 0.002, rot=(math.radians(-15), 0, 0))
# lights: hall ambience + booth spots
light((-3, -4, 5), 2500, 5); light((3, -3, 4), 1200, 4); light((0, 0.5, 3.4), 800, 2)
camera((-2.9, -4.4, 2.05), (0.05, 0.4, 1.15), lens=32)
render('/home/claude/renders/out/trade-show-booth.jpg')
