import bpy, math, json, os
from mathutils import Vector
from pathlib import Path
from math import sin, cos, pi
OUT=Path('/workspace/shared/wichelsee/build/deliverables');OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for x in list(bpy.data.collections):
 if x.name!='Collection':bpy.data.collections.remove(x)
base=bpy.data.collections.get('Collection');base.name='BICYCLE | Wichelsee blockout'
studio=bpy.data.collections.new('STUDIO | excluded from GLB');bpy.context.scene.collection.children.link(studio)
COL=base

def mat(name,c,rough=.4,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 return m
sage=mat('Frame | sage green enamel',(0.10,.28,.15),.3,.18)
black=mat('Components | satin charcoal',(.018,.023,.027),.35,.2)
rubber=mat('Tire | dark rubber',(.014,.017,.02),.79,0)
tan=mat('Tire | restrained natural tan sidewalls',(.25,.12,.052),.82,0)
brown=mat('Bar tape | brown leather-textured tone',(.063,.022,.018),.82,0)
bagmat=mat('Bag | black textile',(.014,.019,.021),.94,0)
silver=mat('Hardware | brushed steel',(.40,.46,.48),.28,.8)
chainmat=mat('Chain | steel',(.27,.31,.33),.4,.72)
spokemat=mat('Spokes | black stainless',(.055,.063,.069),.42,.68)
zipmat=mat('Bag | piping',(.052,.066,.07),.88,0)
white=mat('Studio | warm neutral',(.7,.72,.71),.84)

root=bpy.data.objects.new('WICHELSEE | centered ground origin',None);COL.objects.link(root)
root['status']='FIRST CHECKPOINT: photo-informed blockout, dimensions inferred, not final reconstruction'
root['axes']='Blender +X front, +Z up; drivetrain -Y. GLB +X front,+Y up,drivetrain +Z.'
root['scale']='Meters; assumed tire outside diameter 0.714 m; wheelbase derived 1.048 m'

def reg(o,name,material=None,parent=root):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 COL.objects.link(o)
 if material:o.data.materials.append(material)
 if parent:
  o.parent=parent
 return o

def mesh(name,verts,faces,material,parent=root,smooth=True):
 m=bpy.data.meshes.new(name+' mesh');m.from_pydata(verts,[],faces);m.update()
 o=bpy.data.objects.new(name,m);COL.objects.link(o)
 if material:m.materials.append(material)
 if parent:
  o.parent=parent
 if smooth:
  for p in m.polygons:p.use_smooth=True
 return o

def cyl(name,a,b,r,ma,r2=None,n=16,parent=root):
 a,b=Vector(a),Vector(b);d=b-a
 bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=(a+b)/2)
 o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();reg(o,name,ma,parent)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o

def cube(name,loc,scale,ma,bevel=.004,parent=root):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);reg(o,name,ma,parent)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=bevel;m.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=m.name)
  for p in o.data.polygons:p.use_smooth=True
 return o

def curvepoints(points,steps=5):
 ps=[Vector(points[0])]+[Vector(p) for p in points]+[Vector(points[-1])];out=[]
 for i in range(1,len(ps)-2):
  p0,p1,p2,p3=ps[i-1:i+3]
  for j in range(steps):
   t=j/steps;out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 out.append(Vector(points[-1]));return out

def pipe(name,points,r,ma,n=10,smoothpath=True,parent=root,ellipse=1,rend=None):
 ps=curvepoints(points) if smoothpath else [Vector(p) for p in points];verts=[];faces=[]
 for i,p in enumerate(ps):
  d=(ps[min(i+1,len(ps)-1)]-ps[max(i-1,0)]).normalized(); ref=Vector((0,1,0))
  if abs(d.dot(ref))>.94:ref=Vector((0,0,1))
  u=d.cross(ref).normalized();v=d.cross(u).normalized();rr=r if rend is None else r+(rend-r)*i/(len(ps)-1)
  for j in range(n):
   a=j*2*pi/n;verts.append(tuple(p+rr*cos(a)*u+rr*ellipse*sin(a)*v))
 for i in range(len(ps)-1):
  for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 faces += [tuple(range(n-1,-1,-1)),tuple((len(ps)-1)*n+j for j in range(n))]
 return mesh(name,verts,faces,ma,parent)

def ring(name,center,profile,ma,n=96,parent=root,material_ids=None):
 cx,cy,cz=center;verts=[];faces=[]
 for i in range(n):
  a=2*pi*i/n
  for r,y in profile:verts.append((cx+r*cos(a),cy+y,cz+r*sin(a)))
 k=len(profile)
 for i in range(n):
  for j in range(k):faces.append((i*k+j,((i+1)%n)*k+j,((i+1)%n)*k+(j+1)%k,i*k+(j+1)%k))
 o=mesh(name,verts,faces,ma,parent)
 if material_ids:
  o.data.materials.append(tan)
  for p in o.data.polygons:p.material_index=material_ids[p.index%k]
 return o

def empty(name,loc,parent=root):
 o=bpy.data.objects.new(name,None);COL.objects.link(o);o.location=loc;o.empty_display_size=.055
 if parent:o.parent=parent
 return o

# Image-derived landmarks in a 1366 x 2048 reference coordinate system.
# Equal-wheel reconstruction uses averaged axle y, avoiding small photographic perspective offset.
scale=.714/352.0
rear=(-.524,0,.357);front=(.524,0,.357)
def P(x,y,zdepth=0):return ((x-698.5)*scale,zdepth,(1487-y)*scale)
BB=P(646,1339);ST=P(592,1140);SC=P(582,1112);HT=P(840,1085);HB=P(865,1131);SP=P(555,1021)
# Main frame, small stays genuinely on either side of the rear wheel.
cyl('Frame | down tube',BB,HB,.0185,sage,n=24)
cyl('Frame | top tube',ST,HT,.0148,sage,n=24)
cyl('Frame | seat tube',BB,SC,.0155,sage,n=24)
cyl('Frame | head tube',HB,HT,.0195,sage,n=24)
cyl('Frame | bottom bracket shell',(BB[0],-.038,BB[2]),(BB[0],.038,BB[2]),.024,black,n=24)
for sign,label in [(-1,'drive'),(1,'non-drive')]:
 rd=(-.524,sign*.067,.357)
 pipe('Frame | '+label+' chainstay',[(BB[0],sign*.031,BB[2]),(-.24,sign*.065,.319),rd],.013,sage,n=14,rend=.009)
 pipe('Frame | '+label+' seatstay',[ST,(-.29,sign*.047,.624),rd],.0087,sage,n=12,rend=.0065)
 cyl('Frame | '+label+' dropout',(-.524,sign*.063,.357),(-.524,sign*.077,.357),.019,sage,n=16)
# Fork: no suspension, flattened curved legs, real spacing around tire.
for sign,label in [(-1,'right'),(1,'left')]:
 pipe('Fork | '+label+' rigid blade',[(HB[0]+.006,sign*.038,HB[2]-.008),(.386,sign*.052,.598),(.445,sign*.055,.468),(.524,sign*.053,.357)],.025,black,n=16,ellipse=.47,rend=.013)
 cyl('Fork | '+label+' axle eye',(.524,sign*.048,.357),(.524,sign*.062,.357),.017,black,n=16)
pipe('Fork | crown arch',[(HB[0]+.015,-.039,HB[2]-.027),(HB[0],0,HB[2]),(HB[0]+.015,.039,HB[2]-.027)],.02,black,n=16)
# Headset and cockpit stem.
axis=(Vector(HT)-Vector(HB)).normalized()
for k,point in [('lower',HB),('upper',HT)]:cyl('Headset | '+k,Vector(point)-axis*.004,Vector(point)+axis*.005,.024,black,n=24)
stem_base=Vector(HT)+axis*.075
cyl('Cockpit | steerer',HT,stem_base,.0158,black,n=20)
barcenter=Vector((.347,0,.921))
cyl('Cockpit | stem',stem_base,barcenter,.020,black,n=20)
cyl('Cockpit | stem faceplate',(.347,-.025,.921),(.347,.025,.921),.021,black,n=20)
# True compact dropbar with inferred 420 mm hood / 460 mm drop width.
pipe('Cockpit | exposed center bar',[(.347,-.068,.921),(.347,.068,.921)],.0158,black,n=16,smoothpath=False)
for s,label in [(-1,'drive-side'),(1,'opposite-side')]:
 pts=[(.347,s*.066,.921),(.347,s*.157,.921),(.363,s*.204,.927),(.414,s*.21,.923),(.452,s*.212,.899),(.450,s*.219,.854),(.407,s*.228,.818),(.330,s*.23,.801)]
 pipe('Handlebar | '+label+' brown wrapped drop',pts,.0148,brown,n=14)
 pipe('Controls | '+label+' hood',[(.400,s*.21,.925),(.460,s*.21,.953),(.478,s*.21,.995)],.021,black,n=14,ellipse=.83,rend=.014)
 pipe('Controls | '+label+' brake lever',[(.476,s*.217,.951),(.485,s*.223,.908),(.480,s*.229,.853)],.007,black,n=10,ellipse=.5,rend=.004)
 # cable loops route toward head tube.
 pipe('Cables | '+label+' front loop',[(.463,s*.202,.928),(.438,s*.12,.87),(.35,s*.053,.80),(.336,s*.041,.75)],.0024,black,n=6)
 cyl('Handlebar | '+label+' end plug',(.329,s*.23,.8),(.337,s*.23,.803),.013,black,n=14)
# Tall seatpost and a shaped thin saddle.
cyl('Seatpost | exposed',SC,SP,.0136,black,n=24)
cyl('Seatpost | collar',Vector(SC)-Vector((0,0,.004)),Vector(SC)+Vector((0,0,.004)),.019,black,n=24)
cyl('Seatpost | clamp bolt',(SC[0]-.007,-.022,SC[2]),(SC[0]-.007,.022,SC[2]),.004,silver,n=12)
for s in [-1,1]:pipe('Saddle | rail '+str(s),[(-.39,s*.028,.967),(-.31,s*.026,.944),(-.2,s*.018,.962)],.0035,silver,n=8)
sections=[(-.420,.030,.996),(-.407,.061,.989),(-.377,.073,.974),(-.334,.070,.970),(-.29,.046,.979),(-.245,.025,.982),(-.180,.018,.978),(-.163,.004,.974),(-.160,.0008,.974)]
verts=[];faces=[];n=12
for x,w,z in sections:
 for i in range(n):
  t=2*pi*i/n;verts.append((x,w*cos(t),z+.014*sin(t)))
for a in range(len(sections)-1):
 for j in range(n):faces.append((a*n+j,a*n+(j+1)%n,(a+1)*n+(j+1)%n,(a+1)*n+j))
faces += [tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]
mesh('Saddle | contoured black shell',verts,faces,black)
# Wheels: tires/rims/spokes/hubs remain grouped around exact axle pivots.
for center,label in [(rear,'Rear'),(front,'Front')]:
 pivot=empty('Wheel_'+label+' | axle pivot',center)
 # build world geometry, then preserve transforms when parenting to axle.
 objs=[]
 profile=[(.337+.020*cos(2*pi*j/16),.0215*sin(2*pi*j/16)) for j in range(16)]
 mats=[0 if abs(cos(2*pi*(j+.5)/16))>.71 else 1 for j in range(16)]
 objs.append(ring('Wheel_'+label+' | tire',center,profile,rubber,128,material_ids=mats))
 objs.append(ring('Wheel_'+label+' | rim',center,[(.318,-.013),(.315,-.016),(.290,-.013),(.284,-.007),(.284,.007),(.290,.013),(.315,.016),(.318,.013)],black,128))
 objs.append(cyl('Wheel_'+label+' | hub',(center[0],-.053,center[2]),(center[0],.053,center[2]),.014,black,n=24))
 for s in [-1,1]:
  objs.append(cyl('Wheel_'+label+' | hub flange '+str(s),(center[0],s*.037-.002,center[2]),(center[0],s*.037+.002,center[2]),.024,black,n=24))
  for j in range(16):
   a=2*pi*(j+(0 if s<0 else .5))/16;b=a+( .37 if j%2==0 else -.37)
   p=(center[0]+.023*cos(a),s*.038,center[2]+.023*sin(a));q=(center[0]+.293*cos(b),s*.006,center[2]+.293*sin(b))
   objs.append(cyl('Wheel_'+label+' | spoke '+str(s)+' '+str(j),p,q,.00095,spokemat,n=6))
 # Thin bead ring and valve geometry.
 for s in [-1,1]:objs.append(ring('Wheel_'+label+' | bead '+str(s),center,[(.319,s*.015),(.321,s*.015),(.321,s*.016),(.319,s*.016)],rubber,128))
 objs.append(cyl('Wheel_'+label+' | valve',(center[0],0,center[2]-.285),(center[0],0,center[2]-.268),.0022,silver,n=8))
 # Keep blockout tread a continuous volumetric tire; micro tread left for detail stage.
 bpy.context.view_layer.update()
 for o in objs:
  mw=o.matrix_world.copy();o.parent=pivot;o.matrix_world=mw
 # Left/non-drive brake rotor with open spider.
 cy=.042
 ring('Brake_'+label+' | steel rotor band',(center[0],cy,center[2]),[(.07,-.001),(.083,-.001),(.083,.001),(.07,.001)],silver,96)
 for j in range(6):
  a=j*pi/3
  pipe('Brake_'+label+' | rotor spider '+str(j),[(center[0]+.017*cos(a),cy,center[2]+.017*sin(a)),(center[0]+.046*cos(a+.19),cy,center[2]+.046*sin(a+.19)),(center[0]+.074*cos(a+.2),cy,center[2]+.074*sin(a+.2))],.004,black,n=6)
 cal=(center[0]-.055,.050,center[2]+.054)
 cube('Brake_'+label+' | caliper',cal,(.035,.032,.044),black,.006)
# Bag: closed volumetric wedge, lightly rounded corners and actual straps.
outline=[P(605,1140),P(833,1097),P(832,1115),P(787,1158),P(748,1155),P(681,1170),P(610,1190)]
verts=[(x,s*.035,z) for s in [-1,1] for x,y,z in outline];k=len(outline)
faces=[tuple(range(k-1,-1,-1)),tuple(k+j for j in range(k))]+[(j,(j+1)%k,(j+1)%k+k,j+k) for j in range(k)]
o=mesh('Frame bag | fitted wedge volume',verts,faces,bagmat,smooth=False)
bev=o.modifiers.new('Soft textile edge','BEVEL');bev.width=.009;bev.segments=3;bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=bev.name);o.select_set(False)
for side in [-1,1]:
 pipe('Frame bag | zipper '+str(side),[(outline[0][0],side*.036,outline[0][2]-.005),(outline[1][0],side*.036,outline[1][2]-.005)],.0024,zipmat,n=8,smoothpath=False)
 pipe('Frame bag | bottom seam '+str(side),[(outline[i][0],side*.035,outline[i][2]+.005) for i in [2,3,4,5]],.0015,zipmat,n=6)
for t in [.06,.37,.66,.96]:
 pos=Vector(ST).lerp(Vector(HT),t)
 a=Vector(HT)-Vector(ST);d=a.normalized()
 # Black strap wraps in a plane perpendicular to top tube.
 u=Vector((0,1,0));v=d.cross(u).normalized();vs=[];fs=[]
 for j in range(24):
  ang=2*pi*j/24
  for w in [-.011,.011]:vs.append(tuple(pos+d*w+u*.024*cos(ang)+v*.021*sin(ang)))
 for j in range(24):fs.append((j*2,(j*2+2)%48,(j*2+3)%48,j*2+1))
 mesh('Frame bag | top strap '+str(round(t,2)),vs,fs,bagmat)
for zz in [.634,.679]:
 x=BB[0]+(SC[0]-BB[0])*(zz-BB[2])/(SC[2]-BB[2]);cyl('Frame bag | seat strap '+str(zz),(x,0,zz-.011),(x,0,zz+.011),.0185,bagmat,n=24)
# Wire bottle cages, approximated from visible silver loops, distinct from black mini-pump.
for label,origin,angle in [('seat',(-.105,0,.427),-.24),('down',(-.015,0,.455),.69)]:
 origin=Vector(origin);up=Vector((sin(angle),0,cos(angle)));out=Vector((cos(angle),0,-sin(angle)))
 def cage(u,v,w):return tuple(origin+up*u+Vector((0,v,0))+out*w)
 for s in [-1,1]:pipe('Bottle cage | '+label+' rail '+str(s),[cage(0,s*.026,.00),cage(.0,s*.032,.04),cage(.043,s*.035,.066),cage(.105,s*.032,.050),cage(.156,s*.03,.03)],.0023,silver,n=8)
 pipe('Bottle cage | '+label+' base',[cage(.02,-.035,.04),cage(.005,0,.050),cage(.02,.035,.04)],.0023,silver,n=8)
 # two mount bolts
 for t in [.022,.08]:cyl('Bottle cage | '+label+' mount',cage(t,0,-.008),cage(t,0,.01),.004,silver,n=10)
pipe('Accessories | black mini pump',[P(698,1272,-.021),P(752,1205,-.021)],.010,black,n=12)
# Drive-side crankset and cassette are not mirrored to non-drive.
cx,_,cz=BB;dy=-.062
ring('Drivetrain | single chainring',(cx,dy,cz),[(.066,-.003),(.079,-.003),(.079,.003),(.066,.003)],silver,80)
for j in range(5):
 a=2*pi*j/5
 cyl('Drivetrain | spider arm '+str(j),(cx+.017*cos(a),dy,cz+.017*sin(a)),(cx+.069*cos(a+.10),dy,cz+.069*sin(a+.10)),.008,black,n=8)
for j in range(40):
 a=j*2*pi/40
 cyl('Drivetrain | chainring tooth '+str(j),(cx+.077*cos(a),dy,cz+.077*sin(a)),(cx+.082*cos(a),dy,cz+.082*sin(a)),.002,silver,n=6)
for s in [-1,1]:
 end=(cx+s*-.167,s*.069,cz+s*-.048)
 pipe('Crank | '+('drive' if s<0 else 'non-drive')+' arm',[(cx,s*.061,cz),(cx+s*-.10,s*.068,cz+s*-.029),end],.016,black,n=10,ellipse=.50,rend=.009)
 cyl('Crank | '+str(s)+' axle cap',(cx,s*.063,cz),(cx,s*.071,cz),.015,black,n=20)
 cyl('Pedal | '+str(s)+' spindle',end,(end[0],s*.10,end[2]),.006,silver,n=12)
 cube('Pedal | '+str(s)+' body',(end[0],s*.108,end[2]),(.070,.064,.019),black,.003)
 for k in [-1,1]:cube('Pedal | '+str(s)+' cage '+str(k),(end[0]+k*.028,s*.108,end[2]+.008),(.007,.058,.01),silver,.002)
# 11-sprocket cassette silhouette, count inferred and explicitly provisional.
for j in range(11):
 rr=.097-(j/10)*.069;y=-.036-j*.0038
 ring('Cassette | sprocket '+str(j+1),(-.524,y,.357),[(rr-.008,-.0011),(rr,-.0011),(rr,.0011),(rr-.008,.0011)],silver,64)
 for k in range(6):
  a=k*pi/3;cyl('Cassette | '+str(j)+' spoke '+str(k),(-.524+.017*cos(a),y,.357+.017*sin(a)),(-.524+(rr-.004)*cos(a),y,.357+(rr-.004)*sin(a)),.0025,chainmat,n=6)
# Rear derailleur and two real pulley wheels.
pipe('Derailleur | upper body',[(-.50,-.077,.348),(-.504,-.095,.29),(-.474,-.095,.266)],.018,black,n=10)
for x,z,label in [(-.474,.258,'upper'),(-.485,.168,'lower')]:
 ring('Derailleur | '+label+' pulley',(x,-.082,z),[(.012,-.004),(.018,-.004),(.018,.004),(.012,.004)],black,32)
 cyl('Derailleur | '+label+' pulley axle',(x,-.089,z),(x,-.075,z),.004,silver,n=10)
for s in [-.088,-.076]:pipe('Derailleur | cage '+str(s),[(-.474,s,.268),(-.468,s,.234),(-.485,s,.168)],.007,black,n=8,ellipse=.5)
# True 3D chain loop; blockout rails and spaced rollers rather than flat texture.
chainpath=[(-.524,-.061,.408),(-.30,-.061,.389),(cx-.01,-.062,cz+.080),(cx+.059,-.062,cz+.054),(cx+.081,-.062,cz),(cx+.05,-.062,cz-.061),(-.482,-.082,.150),(-.5,-.082,.167),(-.48,-.082,.241),(-.454,-.082,.26),(-.515,-.061,.317),(-.561,-.061,.35),(-.558,-.061,.394),(-.524,-.061,.408)]
ps=curvepoints(chainpath,5)
for off in [-.003,.003]:pipe('Chain | side rail '+str(off),[(p.x,p.y+off,p.z) for p in ps],.0018,chainmat,n=6,smoothpath=False)
# simple roller links along resampled loop
acc=0
for i in range(len(ps)-1):
 a,b=ps[i],ps[i+1];dist=(b-a).length;count=max(1,int(dist/.012))
 for j in range(count):
  p=a.lerp(b,j/count);cyl('Chain | roller '+str(i)+'-'+str(j),(p.x,p.y-.003,p.z),(p.x,p.y+.003,p.z),.0024,silver,n=6)
# Cable down fork and chainstay retained as separate volumetric strands.
pipe('Cables | front brake hose',[(.315,.035,.81),(.35,.057,.68),(.414,.057,.54),(.467,.058,.411)],.0022,black,n=6)
pipe('Cables | rear brake hose',[(-.50,.07,.41),(-.34,.061,.337),(BB[0],.027,BB[2]+.006),(.13,.026,.55),(.32,.025,.77)],.002,black,n=6)
# Small dark head badge; no invented full brand typography.
badge=cube('Frame | head badge blockout',(HT[0]+.019,0,HT[2]-.026),(.002,.02,.034),black,.001)
# Geometry names and counts; export only bicycle.
bpy.context.view_layer.update()
bike_objs=list(base.objects)
for o in bpy.context.selected_objects:o.select_set(False)
for o in bike_objs:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'RAIL_Wichelsee_blockout.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True)
# Studio is separate from GLB, neutral shape-check lighting.
COL=studio
mesh('Studio ground | excluded from GLB',[(-100,-100,0),(100,-100,0),(100,100,0),(-100,100,0)],[(0,1,2,3)],white,parent=None,smooth=False)
world=bpy.data.worlds.new('Neutral studio world') if not bpy.data.worlds else bpy.data.worlds[0];bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.68,.7,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45

def area(name,loc,energy,size,target):
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Key | large neutral softbox',(-1.5,-3,4),430,4,(0,0,.5));area('Fill | broad',(.5,3,2),330,3,(0,0,.5));area('Rim | broad',(3,1,3),240,2,(0,0,.5))
camdata=bpy.data.cameras.new('Checkpoint camera');cam=bpy.data.objects.new('Checkpoint camera',camdata);studio.objects.link(cam);bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=0
scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS'
views=[('01_drivetrain_side',(0,-4,.525),(0,0,.525),2.10,(1800,1100)),('02_opposite_side',(0,4,.525),(0,0,.525),2.10,(1800,1100)),('03_front',(4,0,.525),(0,0,.525),1.20,(1100,1400)),('04_rear',(-4,0,.525),(0,0,.525),1.20,(1100,1400)),('05_three_quarter',(2.5,-3.6,1.8),(0,0,.50),2.02,(1800,1300))]
# Save before rendering so a recoverable render failure never loses the editable model.
cam.location=views[0][1];cam.rotation_euler=(Vector(views[0][2])-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=2.1
scene.render.resolution_x=1800;scene.render.resolution_y=1100
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'RAIL_Wichelsee_blockout.blend'))
counts={'mesh_objects':sum(o.type=='MESH' for o in bike_objs),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in bike_objs if o.type=='MESH'),'vertices':sum(len(o.data.vertices) for o in bike_objs if o.type=='MESH'),'wheelbase_m':1.048,'tire_diameter_m':.714,'handlebar_drop_width_m':.4896,'origin':'Ground under midpoint between wheel axles','blender_axes':'+X forward / +Z up / drivetrain -Y','gltf_axes':'+X forward / +Y up / drivetrain +Z','external_textures':0}
(OUT/'model_statistics.json').write_text(json.dumps(counts,indent=2))
for name,pos,target,orth,res in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=orth;scene.render.resolution_x,scene.render.resolution_y=res;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Save source in three-quarter inspection position.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'RAIL_Wichelsee_blockout.blend'))
print('FINISHED',json.dumps(counts))
