import bpy, math, json, os
from mathutils import Vector
from pathlib import Path
from math import sin, cos, pi
PROJECT=Path(__file__).resolve().parents[1];OUT=PROJECT;OUT.mkdir(exist_ok=True)
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
root['status']='V2 DETAIL STUDY: reference-based visual approximation; dimensions inferred, not engineering reconstruction'
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

# === V2 refinements ===
import importlib.util, random
from mathutils import Matrix
# Replace coarse assemblies rather than layering a decorative pass over them.
replace_prefixes=['Wheel_','Brake_','Frame bag |','Bottle cage |','Accessories |','Drivetrain |','Cassette |','Derailleur |','Chain |','Crank |','Pedal |','Saddle |','Controls |']
for o in list(base.objects):
 if any(o.name.startswith(p) for p in replace_prefixes):bpy.data.objects.remove(o,do_unlink=True)
black.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.10
black.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.37
silver.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.32
silver.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.30,.33,.35,1)
silver.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.96
spokemat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.025,.031,.033,1)
spokemat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.29
rubber.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.012,.014,.016,1)
# Utility: direct UVs, real beveled profiles, batched boxes.
def uv_planar(o,scale=1,axes=(0,2)):
 uv=o.data.uv_layers.new(name='UVMap')
 for p in o.data.polygons:
  for li in p.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]*scale,v[axes[1]]*scale)
 return o

def uv_ring(o,n,k,uscale=1,vscale=1):
 uv=o.data.uv_layers.new(name='UVMap')
 for f in o.data.polygons:
  i=f.index//k;j=f.index%k
  for li,xy in zip(f.loop_indices,[(i/n,j/k),((i+1)/n,j/k),((i+1)/n,(j+1)/k),(i/n,(j+1)/k)]):uv.data[li].uv=(xy[0]*uscale,xy[1]*vscale)
 return o

def addbox(vs,fs,c,a,b,caxis,sa,sb,sc):
 c,a,b,caxis=Vector(c),Vector(a),Vector(b),Vector(caxis);n=len(vs)
 for z in [-1,1]:
  for y in [-1,1]:
   for x in [-1,1]:vs.append(tuple(c+a*x*sa/2+b*y*sb/2+caxis*z*sc/2))
 fs.extend([tuple(n+i for i in f) for f in [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]])

def smooth_loft(name,sections,ma,n=24):
 # Sections are x, center-y, center-z, y-radius, z-radius. Rounded ends.
 vs=[];fs=[]
 for x,y,z,wy,hz in sections:
  for j in range(n):
   t=j*2*pi/n;vs.append((x,y+wy*cos(t),z+hz*sin(t)))
 for i in range(len(sections)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs += [tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]
 o=mesh(name,vs,fs,ma);bpy.context.view_layer.objects.active=o
 sub=o.modifiers.new('Contour refinement','SUBSURF');sub.levels=1;bpy.ops.object.modifier_apply(modifier=sub.name)
 return uv_planar(o,10)
# Detailed tire/rim and 28-spoke two-cross lacing.
for center,label in [(rear,'Rear'),(front,'Front')]:
 pivot=empty('Wheel_'+label+' | axle pivot',center);pieces=[]
 # Rounded gravel casing: tan lives on sidewalls; crown, shoulders and bead are black.
 half=[(.357,0),(.356,.006),(.353,.012),(.348,.017),(.344,.020),(.338,.0215),(.330,.0208),(.325,.019),(.321,.016),(.317,.012),(.316,.006),(.316,0)]
 profile=[(r-.00056,y) for r,y in half+[(r,-y) for r,y in half[-2:0:-1]]];k=len(profile);mask=[]
 for j in range(k):
  rm=(profile[j][0]+profile[(j+1)%k][0])/2;ym=abs((profile[j][1]+profile[(j+1)%k][1])/2);mask.append(1 if .325<=rm<=.344 and ym>.016 else 0)
 tire=ring('Wheel_'+label+' | rounded gravel casing',center,profile,rubber,192,material_ids=mask);uv_ring(tire,192,k,36,2);pieces.append(tire)
 rimprofile=[(.317,.012),(.315,.014),(.307,.0145),(.290,.0118),(.286,.006),(.286,-.006),(.290,-.0118),(.307,-.0145),(.315,-.014),(.317,-.012),(.313,-.010),(.291,-.004),(.291,.004),(.313,.010)]
 rim=ring('Wheel_'+label+' | satin doublewall rim',center,rimprofile,black,192);uv_ring(rim,192,len(rimprofile),24,1);pieces.append(rim)
 # Fine shallow herringbone knobs; small enough for gravel rather than MTB tread.
 vs=[];fs=[]
 for row,y in enumerate([-.014,-.007,0,.007,.014]):
  rr=.337+.020*math.sqrt(max(0,1-(y/.022)**2))-.00056
  for i in range(224):
   a=(i+(row%2)*.5)*2*pi/224;t=Vector((-sin(a),0,cos(a)));lat=Vector((0,1,0));rad=Vector((cos(a),0,sin(a)))
   angle=(.50 if row%2==0 else -.50);e1=t*cos(angle)+lat*sin(angle);e2=-t*sin(angle)+lat*cos(angle)
   p=Vector(center)+Vector((rr*cos(a),y,rr*sin(a)))+rad*.00028
   addbox(vs,fs,p,e1,e2,rad,.0045,.0018,.00056)
 knobs=mesh('Wheel_'+label+' | fine herringbone tread',vs,fs,rubber,smooth=False);uv_planar(knobs,15);pieces.append(knobs)
 cx,cy,cz=center
 pieces.append(cyl('Wheel_'+label+' | center hub barrel',(cx,-.035,cz),(cx,.035,cz),.0115,black,n=32))
 for s in [-1,1]:
  pieces.append(cyl('Wheel_'+label+' | hub body taper '+str(s),(cx,s*.012,cz),(cx,s*.038,cz),.012,black,r2=.021,n=32))
  pieces.append(cyl('Wheel_'+label+' | flange '+str(s),(cx,s*.0365,cz),(cx,s*.0395,cz),.022,black,n=32))
  pieces.append(cyl('Wheel_'+label+' | endcap '+str(s),(cx,s*.04,cz),(cx,s*.05,cz),.0085,black,n=24))
  for j in range(14):
   ah=2*pi*j/14;ar=2*pi*(j+(2 if j%2==0 else -2))/14+(0 if s<0 else pi/14)
   p=Vector((cx+.021*cos(ah),s*.038,cz+.021*sin(ah)));q=Vector((cx+.291*cos(ar),s*.0045,cz+.291*sin(ar)))
   # Double-butted spoke: actual ~1.6mm center with subtle end thickening.
   spoke=pipe('Wheel_'+label+' | spoke '+str(s)+' '+str(j),[p,p.lerp(q,.09),p.lerp(q,.92),q],.00082,spokemat,n=6,smoothpath=False);pieces.append(spoke)
   nip0=q-Vector((cos(ar),0,sin(ar)))*.004;nip1=q+Vector((cos(ar),0,sin(ar)))*.003
   pieces.append(cyl('Wheel_'+label+' | nipple '+str(s)+' '+str(j),nip0,nip1,.00165,black,n=8))
   pieces.append(cyl('Wheel_'+label+' | spoke head '+str(s)+' '+str(j),(p.x,s*.036,p.z),(p.x,s*.041,p.z),.0018,black,n=8))
 # Valve at reference-like upper sector.
 ang=pi/2+.14
 v0=Vector(center)+Vector((.287*cos(ang),0,.287*sin(ang)));v1=Vector(center)+Vector((.271*cos(ang),0,.271*sin(ang)))
 pieces.append(cyl('Wheel_'+label+' | presta valve',v0,v1,.002,silver,n=10));pieces.append(cyl('Wheel_'+label+' | valve cap',v1,v1-Vector((.005*cos(ang),0,.005*sin(ang))),.0026,black,n=10))
 bpy.context.view_layer.update()
 for o in pieces:
  mw=o.matrix_world.copy();o.parent=pivot;o.matrix_world=mw
# Soft bag shell with controlled fabric bulge and shallow, broad wrinkles.
bagsections=[(0,.602),(.23,.628),(.52,.662),(.72,.672),(.86,.669),(1,.751)]
def bottom(u):
 for (a,z),(b,zz) in zip(bagsections,bagsections[1:]):
  if a<=u<=b:
   t=(u-a)/(b-a);t=t*t*(3-2*t);return z+(zz-z)*t
 return .751

def bagpoint(u,v,side):
 x=-.185+.458*u;top=.702+.093*u;z=bottom(u)+(top-bottom(u))*v
 bulge=.024+.012*(max(0,sin(pi*u))*max(0,sin(pi*v)))**.6
 wrinkle=(.0013*sin(28*u+9*v)+.0009*sin(43*u-13*v))*(sin(pi*u)*sin(pi*v))
 # Local fabric compression radiates from top strap and bottom corner locations.
 wrinkle+=.0018*math.exp(-((u-.12)/.13)**2)*sin(v*17+u*25)*sin(pi*v)
 for tc,dr in [(.08,.13),(.37,-.11),(.68,.15),(.93,-.18)]:
  ridge=u-(tc+dr*(1-v));wrinkle+=.0032*(math.exp(-(ridge/.024)**2)-.58*math.exp(-((ridge+.021)/.026)**2))*sin(pi*v)
 return (x,side*(bulge+wrinkle),z)
nu,nv=70,18;vs=[];fs=[]
for side in [-1,1]:
 for i in range(nu+1):
  for j in range(nv+1):vs.append(bagpoint(i/nu,j/nv,side))
offset=(nu+1)*(nv+1)
for sidx in range(2):
 off=sidx*offset
 for i in range(nu):
  for j in range(nv):
   ids=(off+i*(nv+1)+j,off+(i+1)*(nv+1)+j,off+(i+1)*(nv+1)+j+1,off+i*(nv+1)+j+1);fs.append(ids if sidx==0 else ids[::-1])
for i in range(nu):
 for j in [0,nv]:a=i*(nv+1)+j;b=(i+1)*(nv+1)+j;fs.append((a,b,b+offset,a+offset))
for j in range(nv):
 for i in [0,nu]:a=i*(nv+1)+j;b=a+1;fs.append((a,a+offset,b+offset,b))
bagobj=uv_planar(mesh('Frame bag | soft woven shell',vs,fs,bagmat),15.625)
for side in [-1,1]:
 for label,v in [('upper seam',.985),('lower seam',.025)]:pipe('Frame bag | '+label+' '+str(side),[bagpoint(i/60,v,side) for i in range(61)],.001,zipmat,n=6,smoothpath=False)
 # Closed zipper strip and closely spaced teeth on visible pouch sides.
 points=[Vector(bagpoint(i/70,.89,side))+Vector((0,side*.001,0)) for i in range(71)]
 pipe('Frame bag | zipper tape '+str(side),points,.0025,black,n=6,smoothpath=False,ellipse=.65)
 vs=[];fs=[]
 for i in range(132):
  u=.012+i*.976/132;p=Vector(bagpoint(u,.89,side))+Vector((0,side*.002,0));addbox(vs,fs,p,(1,0,.20),(0,1,0),(-.2,0,1),.00125,.001,.0033)
 mesh('Frame bag | zipper teeth '+str(side),vs,fs,zipmat,smooth=False)
 p=Vector(bagpoint(.96,.89,side));pipe('Frame bag | zipper pull '+str(side),[p+Vector((0,side*.004,0)),p+Vector((-.013,side*.01,-.015)),p+Vector((-.025,side*.01,-.014)),p+Vector((-.014,side*.003,.001))],.0013,black,n=8)
# Straps are closed webbing surfaces, physically looping over the top tube and onto the bag.
for index,t in enumerate([.075,.37,.65,.955]):
 c=Vector(ST).lerp(Vector(HT),t);d=(Vector(HT)-Vector(ST)).normalized();n=d.cross(Vector((0,1,0))).normalized()
 # d cross Y is normal pointing upward for this tube.
 contour=[(-.027,-.035),(-.024,-.005),(-.016,.011),(-.006,.0168),(.006,.0168),(.016,.011),(.024,-.005),(.027,-.035)]
 verts=[];faces=[]
 for yy,nn in contour:
  for w in [-.009,.009]:verts.append(tuple(c+d*w+Vector((0,yy,0))+n*nn))
 for j in range(len(contour)):faces.append((j*2,((j+1)%len(contour))*2,((j+1)%len(contour))*2+1,j*2+1))
 o=uv_planar(mesh('Frame bag | attached top strap '+str(index+1),verts,faces,bagmat),20)
 solid=o.modifiers.new('Webbing thickness','SOLIDIFY');solid.thickness=.0012;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=solid.name)
for index,zz in enumerate([.642,.690]):
 x=BB[0]+(SC[0]-BB[0])*(zz-BB[2])/(SC[2]-BB[2]);p=Vector((x,0,zz));d=(Vector(SC)-Vector(BB)).normalized()
 cyl('Frame bag | seat strap '+str(index+1),p-d*.009,p+d*.009,.0172,bagmat,n=32)
 for sign in [-1,1]:pipe('Frame bag | rear strap anchor '+str(index)+str(sign),[(x,sign*.017,zz),(-.182,sign*.024,zz)],.008,bagmat,n=6,ellipse=.18,smoothpath=False)
# Continuous cage wire and two frame-contact mounts per cage.
for label,tube_a,tube_b,t0 in [('seat',BB,SC,.28),('down',BB,HB,.31)]:
 e=(Vector(tube_b)-Vector(tube_a)).normalized();out=Vector((e.z,0,-e.x)) if label=='seat' else Vector((-e.z,0,e.x));anchor=Vector(tube_a).lerp(Vector(tube_b),t0)
 def C(u,y,v):return tuple(anchor+e*u+Vector((0,y,0))+out*v)
 pipe('Bottle cage | '+label+' backbone',[C(0,0,.021),C(.10,0,.021),C(.17,0,.022)],.0022,silver,n=10)
 for s in [-1,1]:
  pts=[C(.165,s*.030,.045),C(.142,s*.032,.069),C(.111,s*.035,.073),C(.07,s*.034,.055),C(.018,s*.031,.060),C(.002,s*.022,.043),C(.012,0,.023)]
  pipe('Bottle cage | '+label+' shaped rail '+str(s),pts,.0021,silver,n=10)
  pipe('Bottle cage | '+label+' upper bridge '+str(s),[C(.09,0,.021),C(.11,s*.025,.035),C(.142,s*.032,.069)],.0021,silver,n=10)
 for u in [.029,.092]:
  cyl('Bottle cage | '+label+' standoff '+str(u),C(u,0,.014),C(u,0,.024),.0045,black,n=12)
  cyl('Bottle cage | '+label+' bolt '+str(u),C(u,0,.022),C(u,0,.026),.0032,silver,n=12)
# Mini-pump on near side of down tube with two visible rubber saddles.
pa,pb=Vector(P(697,1272,-.027)),Vector(P(751,1205,-.027));cyl('Accessories | pump barrel',pa,pb,.008,black,n=20)
cyl('Accessories | pump handle',pa,pa.lerp(pb,.14),.010,black,n=20)
cyl('Accessories | pump head',pb,pb+(pb-pa).normalized()*.012,.010,black,n=20)
for t in [.20,.76]:
 p=pa.lerp(pb,t);q=Vector((p.x,0,p.z));cyl('Accessories | pump mounting saddle '+str(t),q,p,.009,black,n=12)
# A thin, fully rounded saddle with black rails and subtle shell edge.
ss=[(-.423,0,.994,.002,.002),(-.415,0,.992,.041,.006),(-.396,0,.983,.064,.012),(-.371,0,.973,.072,.014),(-.344,0,.972,.065,.013),(-.310,0,.978,.047,.011),(-.278,0,.980,.028,.007),(-.238,0,.980,.020,.007),(-.196,0,.978,.017,.006),(-.171,0,.975,.011,.004),(-.160,0,.974,.0008,.0008)]
saddle=smooth_loft('Saddle | rounded performance shell',ss,black,32)
for s in [-1,1]:
 pipe('Saddle | black rail '+str(s),[(-.395,s*.024,.967),(-.347,s*.028,.944),(-.305,s*.026,.945),(-.22,s*.017,.965)],.0032,black,n=10)
pipe('Saddle | center relief', [(-.374,0,.982),(-.33,0,.981),(-.28,0,.987)],.0028,black,n=8)
# Ergonomic hood shells, and thin lever blades rather than round tubes.
for s,label in [(-1,'drive-side'),(1,'opposite-side')]:
 sections=[(.392,s*.209,.925,.016,.010),(.410,s*.209,.931,.024,.018),(.438,s*.209,.944,.026,.021),(.461,s*.209,.961,.024,.026),(.478,s*.209,.987,.018,.020),(.490,s*.209,.995,.011,.009)]
 outline=[(.395,.923),(.412,.940),(.444,.950),(.460,.965),(.468,.987),(.478,1.002),(.490,1.001),(.497,.989),(.488,.963),(.486,.942),(.469,.932),(.449,.908),(.425,.903),(.408,.909)]
 vs=[];fs=[];nn=len(outline)
 for side in [-1,1]:
  for x,z in outline:vs.append((x,s*.209+side*(.016 if z>.975 else .023),z))
 vs.extend([(.458,s*.209-.029,.950),(.458,s*.209+.029,.950)])
 fs=[(nn*2,(j+1)%nn,j) for j in range(nn)]+[(nn*2+1,nn+j,nn+(j+1)%nn) for j in range(nn)]+[(j,(j+1)%nn,(j+1)%nn+nn,j+nn) for j in range(nn)]
 hood=mesh('Controls | '+label+' sculpted hood',vs,fs,black,smooth=False);bpy.context.view_layer.objects.active=hood
 bevel=hood.modifiers.new('Ergonomic molded edges','BEVEL');bevel.width=.0048;bevel.segments=4;bevel.limit_method='ANGLE';bevel.angle_limit=.4;bpy.ops.object.modifier_apply(modifier=bevel.name)
 for face in hood.data.polygons:face.use_smooth=True
 uv_planar(hood,20)
 pts=curvepoints([(.477,s*.228,.955),(.480,s*.235,.921),(.482,s*.242,.887),(.496,s*.246,.861)],6);vs=[];fs=[]
 for i,p in enumerate(pts):
  t=i/(len(pts)-1);d=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();n=Vector((-d.z,0,d.x));width=.013*(1-t)+.006*t
  for z in [-1,1]:
   for y in [-1,1]:vs.append(tuple(p+n*z*width/2+Vector((0,y*.0022,0))))
 for i in range(len(pts)-1):
  a=i*4;b=(i+1)*4
  for ids in [(0,1,3,2),(0,2,2,0)]:pass
  fs.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
 fs +=[(0,1,3,2),tuple((len(pts)-1)*4+k for k in [0,2,3,1])]
 mesh('Controls | '+label+' flat brake blade',vs,fs,black)
 cyl('Controls | '+label+' lever pivot',(.477,s*.207,.952),(.477,s*.235,.952),.0037,silver,n=12)
# Fork mount bosses and smooth crown fill, retaining the primary blade silhouette.
for s in [-1,1]:
 for j,t in enumerate([.22,.45,.68]):
  a=Vector((HB[0]+.006,s*.050,HB[2]-.008));b=Vector((.524,s*.055,.357));p=a.lerp(b,t)
  cyl('Fork | cargo boss '+str(s)+' '+str(j),(p.x,s*.059,p.z),(p.x,s*.063,p.z),.0038,black,n=12)
# Small, photo-supported WHISKY lettering as actual decal-thin geometry.
letter=mat('Lettering | warm off-white',(.65,.69,.66),.55,0)
def text_label(name,body,loc,xdir,normal,size,ma):
 data=bpy.data.curves.new(name,'FONT');data.body=body;data.size=size;data.extrude=.000015;data.align_x='CENTER';data.align_y='CENTER';data.font=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf') if Path('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf').exists() else bpy.data.fonts.get('Bfont')
 o=bpy.data.objects.new(name,data);COL.objects.link(o);o.location=loc;x=Vector(xdir).normalized();n=Vector(normal).normalized();y=n.cross(x).normalized();o.rotation_euler=Matrix(((x.x,y.x,n.x),(x.y,y.y,n.y),(x.z,y.z,n.z))).to_euler();data.materials.append(ma);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.parent=root;o.select_set(False);return o
for s in [-1,1]:text_label('Fork | WHISKY marking '+str(s),'WHISKY',(.476,s*.063,.436),(.37,0,-.93),(0,s,0),.0105,letter)
# Give basic tube UVs to existing frame and cockpit objects; texture hookups follow later.
for o in base.objects:
 if o.type=='MESH' and not o.data.uv_layers:uv_planar(o,10)
# External module supplies meaningful flat mechanical profiles and articulated chain geometry.
if not os.environ.get('SKIP_MECH'):
 spec=importlib.util.spec_from_file_location('mechanics',str(PROJECT/'scripts/mechanics.py'));mechanics=importlib.util.module_from_spec(spec);spec.loader.exec_module(mechanics)
 mechanics.build_mechanics(globals())
# Texture application, export and rendering are appended by the coordinator.
# Embedded image-based PBR maps; no procedural Blender-only texture dependencies.
TEX=PROJECT/'textures'
def image_node(nodes,prefix,suffix,color):
 n=nodes.new('ShaderNodeTexImage');im=bpy.data.images.load(str(TEX/(prefix+'_'+suffix+'.png')),check_existing=True);im.colorspace_settings.name='sRGB' if color else 'Non-Color';n.image=im;n.extension='REPEAT';im.pack();return n

def hook_pbr(ma,prefix,normal_strength=1,base_color=True):
 ns=ma.node_tree.nodes;ls=ma.node_tree.links;bs=ns.get('Principled BSDF');bs.inputs['Metallic'].default_value=0
 if base_color:
  col=image_node(ns,prefix,'basecolor',True);ls.new(col.outputs['Color'],bs.inputs['Base Color'])
 rough=image_node(ns,prefix,'roughness',False);ls.new(rough.outputs['Color'],bs.inputs['Roughness'])
 normal=image_node(ns,prefix,'normal',False);nm=ns.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=normal_strength;ls.new(normal.outputs['Color'],nm.inputs['Color']);ls.new(nm.outputs['Normal'],bs.inputs['Normal'])
hook_pbr(bagmat,'nylon_black',.8);hook_pbr(rubber,'rubber_black',.65);hook_pbr(brown,'tape_dark_chocolate',.8);hook_pbr(sage,'enamel_sage',.35);hook_pbr(tan,'rubber_black',.4,False)
# Keep restrained caramel pigment on uncoated sidewall, a distinct PBR material.
tan.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.25,.13,.075,1)
for o in base.objects:
 if o.type=='MESH' and not o.data.uv_layers:uv_planar(o,15)
 if o.type=='MESH' and o.name.startswith('Handlebar |') and 'brown' in o.name:
  n=14;k=len(o.data.vertices)//n;uv=o.data.uv_layers.active;centers=[sum((o.data.vertices[i*n+j].co for j in range(n)),Vector())/n for i in range(k)];lengths=[0]
  for a,b in zip(centers,centers[1:]):lengths.append(lengths[-1]+(b-a).length)
  for f in o.data.polygons:
   if f.index>=(k-1)*n:continue
   i=f.index//n;j=f.index%n
   for li,(u,v) in zip(f.loop_indices,[(lengths[i]/.04,j/n*2.325),(lengths[i]/.04,(j+1)/n*2.325),(lengths[i+1]/.04,(j+1)/n*2.325),(lengths[i+1]/.04,j/n*2.325)]):uv.data[li].uv=(u,v)
# Photo-supported RAIL badge on the forward head tube surface.
htmid=(Vector(HT)+Vector(HB))/2;normal=Vector((.878,0,.477));xdir=Vector((0,1,0));up=normal.cross(xdir);bc=htmid+normal*.0205
for o in list(base.objects):
 if o.name=='Frame | head badge blockout':bpy.data.objects.remove(o,do_unlink=True)
vs=[tuple(bc+xdir*x*.014+up*z*.025) for z in [-1,1] for x in [-1,1]]
mesh('Frame | black head badge',vs,[(0,1,3,2)],black,smooth=False)
text_label('Frame | RAIL head badge','RAIL',htmid+normal*.0213,xdir,normal,.009,letter)
for side in [-1,1]:
 text_label('Headset | KING marking '+str(side),'KING',Vector(HT)+Vector((0,side*.024,.003)),(1,0,.2),(0,side,0),.005,letter)
# Preview/export studio is separate from bicycle.
COL=studio
mesh('Studio ground | excluded from GLB',[(-100,-100,-.001),(100,-100,-.001),(100,100,-.001),(-100,100,-.001)],[(0,1,2,3)],white,parent=None,smooth=False)
world=bpy.data.worlds.new('Neutral studio') if not bpy.data.worlds else bpy.data.worlds[0];bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.68,.70,.69,1);world.node_tree.nodes['Background'].inputs[1].default_value=.4

def area(name,loc,energy,size,target):
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Key | broad neutral',(-1.8,-3,4),430,4,(0,0,.5));area('Fill | neutral',(.5,3,2.8),230,3,(0,0,.5));area('Rim | neutral',(3,.8,3),240,2.5,(0,0,.5))
camdata=bpy.data.cameras.new('Inspection camera');cam=bpy.data.objects.new('Inspection camera',camdata);studio.objects.link(cam);scene=bpy.context.scene;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False;scene.cycles.use_adaptive_sampling=True;scene.cycles.adaptive_threshold=.012
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.unit_settings.system='METRIC'
cam.location=(2.5,-3.6,1.55);cam.rotation_euler=(Vector((0,0,.51))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=2.04;scene.render.resolution_x=1800;scene.render.resolution_y=1300
bpy.context.view_layer.update()
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
source=OUT/'RAIL_Wichelsee_visual_v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
# Render new material/geometry previews before any optimization or delivery.
if not os.environ.get('NO_PREVIEW'):
 scene.render.filepath=str(OUT/'preview_v2_three_quarter.png');bpy.ops.render.render(write_still=True)
 cam.location=(0,-4,.525);cam.rotation_euler=(Vector((0,0,.525))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.ortho_scale=2.1;scene.render.resolution_x=1800;scene.render.resolution_y=1100;scene.render.filepath=str(OUT/'preview_v2_side.png');bpy.ops.render.render(write_still=True)
 print('V2_PREVIEW_READY')
