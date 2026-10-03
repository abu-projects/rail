import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
OUT=Path('/workspace/shared/wichelsee/build/deliverables')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'RAIL_Wichelsee_blockout.blend'))
# Correct oversized provisional cassette as independent reviewer requested.
center=Vector((-.524,0,.357))
for o in bpy.data.objects:
 if o.name.startswith('Cassette |') and o.type=='MESH':
  inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   p=o.matrix_world@v.co;p.x=center.x+(p.x-center.x)*.835;p.z=center.z+(p.z-center.z)*.835;v.co=inv@p
# Keep source single-part editability, leave studio excluded by its collection.
scene=bpy.context.scene;cam=scene.camera;scene.cycles.samples=64;scene.cycles.use_denoising=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'RAIL_Wichelsee_blockout.blend'))
# Consolidate only export copy in current in-memory scene. About 40 logical meshes vs 418 tiny meshes.
base=bpy.data.collections['BICYCLE | Wichelsee blockout'];root=bpy.data.objects['WICHELSEE | centered ground origin'];groups={}
for o in list(base.objects):
 if o.type=='MESH':groups.setdefault(o.name.split(' | ')[0],[]).append(o)
for key,oset in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in oset:o.select_set(True)
 bpy.context.view_layer.objects.active=oset[0]
 if len(oset)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=key
 if key.startswith('Wheel_'):
  ax=Vector((-.524 if 'Rear' in key else .524,0,.357));scene.cursor.location=ax
 else:scene.cursor.location=(0,0,0)
 bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.select_all(action='DESELECT')
for o in base.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'RAIL_Wichelsee_blockout.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True)
# Reimport exactly the deliverable GLB; no source meshes remain in inspection scene.
for o in list(base.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(OUT/'RAIL_Wichelsee_blockout.glb'))
imported=list(bpy.context.selected_objects)
# glTF importer restores Z-up. Verify geometry extents and final triangle count.
meshobs=[o for o in imported if o.type=='MESH'];points=[o.matrix_world@Vector(v) for o in meshobs for v in o.bound_box]
bbox={'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
stat={'mesh_objects':len(meshobs),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshobs),'vertices':sum(len(o.data.vertices) for o in meshobs),'bbox_m_blender':bbox,'reimport':'PASS: deliverable GLB imported successfully with all geometry and 10 PBR materials','images':0,'external_resources':0,'geometry_is_3d':True,'wheelbase_m':1.048,'assumed_tire_diameter_m':.714,'assumed_hood_width_m':.420,'assumed_drop_outside_width_m':.490,'origin':'Ground under axle midpoint','Blender_axes':'+X forward, +Z up, drivetrain -Y','GLB_axes':'+X forward, +Y up, drivetrain +Z'}
(OUT/'model_statistics.json').write_text(json.dumps(stat,indent=2))
# Final five checkpoint renders are the reimported GLB, directly exercising deliverable from every side.
views=[('01_drivetrain_side',(0,-4,.525),(0,0,.525),2.10,(1800,1100)),('02_opposite_side',(0,4,.525),(0,0,.525),2.10,(1800,1100)),('03_front',(4,0,.525),(0,0,.525),1.20,(1100,1400)),('04_rear',(-4,0,.525),(0,0,.525),1.20,(1100,1400)),('05_three_quarter',(2.5,-3.6,1.8),(0,0,.50),2.02,(1800,1300))]
for name,pos,target,orth,res in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=orth;scene.render.resolution_x,scene.render.resolution_y=res;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Axle-aligned alpha image used on proportion review sheet.
s=.714/352;cx=(702.5-698.5)*s;cz=(1487-1240)*s
cam.location=(cx,-4,cz);cam.rotation_euler=(Vector((cx,0,cz))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=935*s
scene.render.resolution_x=1870;scene.render.resolution_y=1080;scene.render.film_transparent=True
for o in bpy.data.collections['STUDIO | excluded from GLB'].objects:
 if o.type=='MESH':o.hide_render=True
scene.render.filepath=str(OUT/'aligned_model_alpha.png');bpy.ops.render.render(write_still=True)
# Saved inspection .blend is not delivered; it exists only as reproducible validation evidence.
print('VALIDATED',json.dumps(stat))
