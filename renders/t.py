import bpy,time
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.device='CPU'; s.cycles.samples=32; s.cycles.use_denoising=True
bpy.ops.mesh.primitive_cube_add(size=1); 
bpy.ops.object.light_add(type='AREA',location=(2,-2,3)); bpy.context.object.data.energy=500
bpy.ops.object.camera_add(location=(3,-3,2),rotation=(1.1,0,0.78)); s.camera=bpy.context.object
s.render.resolution_x=400; s.render.resolution_y=300; s.render.filepath='/home/claude/renders/t.png'
t=time.time(); bpy.ops.render.render(write_still=True); print('time',time.time()-t)
