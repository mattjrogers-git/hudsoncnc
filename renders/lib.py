import bpy, math, random
from mathutils import Vector

def reset(samples=96, res=(1600, 1200)):
    import os
    res = (int(os.environ.get('RW', res[0])), int(os.environ.get('RH', res[1])))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'
    s.cycles.samples = samples; s.cycles.use_denoising = True
    s.cycles.max_bounces = 6
    s.render.resolution_x, s.render.resolution_y = res
    s.view_settings.view_transform = 'Filmic' if 'Filmic' in [i.identifier for i in s.view_settings.bl_rna.properties['view_transform'].enum_items] else 'AgX'
    s.view_settings.look = 'None'
    s.view_settings.exposure = -0.6
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.92, 0.93, 0.95, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.18
    return s

def mat(name, color, rough=0.5, metal=0.0, bump=None, noise=None, coat=0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat
    if noise:  # (scale, strength) color variation
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = noise[0]
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = noise[1]
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        mix.inputs[6].default_value = (*color, 1)
        nt.links.new(nz.outputs['Color'], mix.inputs[7])
        nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    if bump:
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = bump[0]; nz.inputs['Detail'].default_value = 8
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump[1]
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
        nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def wood(name='ply', c1=(0.80, 0.64, 0.44), c2=(0.62, 0.45, 0.28), scale=(1, 18, 1), ring=6.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.55
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = scale
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = ring
    wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 3
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    cr.color_ramp.elements[0].position = 0.35
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m

def osb(name='osb'):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.8
    tc = nt.nodes.new('ShaderNodeTexCoord'); vr = nt.nodes.new('ShaderNodeTexVoronoi'); vr.inputs['Scale'].default_value = 28
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 3, 1)
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (0.55, 0.38, 0.18, 1); cr.color_ramp.elements[1].color = (0.82, 0.66, 0.42, 1)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], vr.inputs['Vector'])
    nt.links.new(vr.outputs['Color'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m

def box(name, size, loc, m, bevel=0.002, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv = o.modifiers.new('b', 'BEVEL'); bv.width = bevel; bv.segments = 2
    o.data.materials.append(m); return o

def cyl(name, r, h, loc, m, rot=(0, 0, 0), verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o

def cone(name, r1, r2, h, loc, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, location=loc, rotation=rot, vertices=32)
    o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

def text(s, loc, size, m, rot=(math.radians(90), 0, 0), extrude=0.002, align='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.data.body = s; o.data.size = size; o.data.extrude = extrude
    o.data.align_x = align; o.data.align_y = 'CENTER'
    o.data.materials.append(m); return o

def studio(floor_col=(0.86, 0.87, 0.88), wall=True):
    fm = mat('floor', floor_col, rough=0.7)
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0)); bpy.context.object.data.materials.append(fm)
    if wall:
        bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 4, 0), rotation=(math.radians(90), 0, 0))
        bpy.context.object.data.materials.append(fm)

def light(loc, energy, size=2.0, rot=None, color=(1, 0.97, 0.92)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object; l.data.energy = energy * 0.22; l.data.size = size; l.data.color = color
    tgt = Vector((0, 0, 0.6)); d = tgt - l.location
    l.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return l

def camera(loc, target, lens=50, dof=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object; c.data.lens = lens
    d = Vector(target) - c.location; c.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = c
    if dof:
        c.data.dof.use_dof = True; c.data.dof.aperture_fstop = dof; c.data.dof.focus_distance = d.length
    return c

def render(path):
    s = bpy.context.scene; s.render.filepath = path
    s.render.image_settings.file_format = 'JPEG'; s.render.image_settings.quality = 90
    bpy.ops.render.render(write_still=True)

PALETTE = dict(blue=(0.08, 0.25, 0.62), orange=(0.85, 0.36, 0.08), charcoal=(0.07, 0.08, 0.09), white=(0.88, 0.88, 0.86))

def tube(loc, body, band, tip, h=0.22, r=0.026, rot=(0, 0, 0), name='tube'):
    """cartridge-style product tube standing on loc (base center)."""
    x, y, z = loc
    cyl(name, r, h, (x, y, z + h / 2), body)
    cyl(name + 'b', r * 1.012, h * 0.55, (x, y, z + h * 0.45), band)
    cone(name + 'n', r * 0.45, r * 0.12, h * 0.42, (x, y, z + h + h * 0.21), tip)
    cyl(name + 'c', r * 0.98, 0.012, (x, y, z + 0.006), tip)

def mini_cutaway(ox, oy, oz, s=1.0, mats=None):
    ply, stud, ins, osbm, wrap, side = mats
    H = 1.0 * s
    box('mc_base', (0.9 * s, 0.4 * s, 0.08 * s), (ox, oy, oz + 0.04 * s), ply)
    z0 = oz + 0.08 * s
    for x in (-0.4, -0.1, 0.2):
        box('mc_stud', (0.038 * s, 0.089 * s, H), (ox + x * s, oy, z0 + H / 2), stud)
    for a, b in ((-0.4, -0.1), (-0.1, 0.2)):
        box('mc_ins', ((b - a - 0.04) * s, 0.085 * s, H - 0.02), (ox + (a + b) / 2 * s, oy, z0 + H / 2), ins, 0.01)
    box('mc_osb', (0.55 * s, 0.011 * s, H), (ox + 0.1 * s, oy - 0.05 * s, z0 + H / 2), osbm, 0)
    box('mc_wrap', (0.4 * s, 0.002 * s, H), (ox + 0.175 * s, oy - 0.057 * s, z0 + H / 2), wrap, 0)
    for k in range(int(H / (0.11 * s))):
        box('mc_sid', (0.25 * s, 0.012 * s, 0.13 * s), (ox + 0.25 * s, oy - 0.075 * s, z0 + 0.07 * s + k * 0.11 * s), side, 0.002, rot=(math.radians(-3), 0, 0))
