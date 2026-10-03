"""Photo-informed v2 Wichelsee drivetrain and brakes.

World coordinates: +X front, +Z up, drive side -Y.  Components are batched
per material.  Dimensions/tooth counts are visual inferences, not OEM CAD.
The only public entry point is build_mechanics(ctx).
"""
import math
from math import sin, cos, pi, atan2, sqrt
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon


def build_mechanics(ctx):
    bpy = ctx['bpy']
    mesh = ctx['mesh']
    cyl, cube, ring = ctx['cyl'], ctx['cube'], ctx['ring']
    root = ctx['root']
    black, silver, chainmat = ctx['black'], ctx['silver'], ctx['chainmat']
    cx, cz = (646 - 698.5) * (.714 / 352), (1487 - 1339) * (.714 / 352)
    rear, front = (-.524, .357), (.524, .357)
    drive_y = -.062
    created = []

    class Batch:
        def __init__(self, name, material):
            self.name, self.material, self.v, self.f = name, material, [], []
        def add(self, verts, faces):
            offset = len(self.v)
            self.v.extend(verts)
            self.f.extend(tuple(offset + x for x in face) for face in faces)
        def solid(self, outline, y, thickness):
            # An actual flat-sided extruded polygon, never a round wire.
            n = len(outline)
            vv = [(x, y - thickness / 2, z) for x, z in outline]
            vv += [(x, y + thickness / 2, z) for x, z in outline]
            poly = [Vector((x, 0, z)) for x, z in outline]
            index = {tuple(p): i for i, p in enumerate(poly)}
            triangles = tessellate_polygon([poly])
            ff = []
            for tri in triangles:
                ids = [v if isinstance(v, int) else index[tuple(v)] for v in tri]
                ff.append(tuple(reversed(ids)))
                ff.append(tuple(i + n for i in ids))
            ff += [(j, (j + 1) % n, (j + 1) % n + n, j + n) for j in range(n)]
            self.add(vv, ff)
        def annulus(self, center, r_inner, r_outer, y, thickness, n=64, phase=0):
            xx, zz = center
            self.radial(center, [r_inner] * n, [r_outer] * n, y, thickness, phase)
        def radial(self, center, inner, outer, y, thickness, phase=0):
            xx, zz = center; n = len(inner); vv = []
            for i in range(n):
                a = phase + 2 * pi * i / n
                for rr, yy in [(inner[i], y-thickness/2), (outer[i], y-thickness/2),
                               (inner[i], y+thickness/2), (outer[i], y+thickness/2)]:
                    vv.append((xx+rr*cos(a), yy, zz+rr*sin(a)))
            ff = []
            for i in range(n):
                a, b = i * 4, ((i + 1) % n) * 4
                ff += [(a, b, b+1, a+1), (a+2, a+3, b+3, b+2),
                       (a+1, b+1, b+3, a+3), (a, a+2, b+2, b)]
            self.add(vv, ff)
        def cylinder(self, center, r, y, length, n=8):
            xx, zz = center
            vv = [(xx+r*cos(2*pi*i/n), y+dy, zz+r*sin(2*pi*i/n))
                  for dy in [-length/2, length/2] for i in range(n)]
            ff = [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
            ff += [tuple(range(n-1,-1,-1)), tuple(range(n,2*n))]
            self.add(vv, ff)
        def finish(self, smooth=False):
            if not self.v: return None
            ob = mesh(self.name, self.v, self.f, self.material, parent=root, smooth=smooth)
            created.append(ob)
            return ob

    dark = Batch('Drivetrain | sculpted asymmetric four-arm spider', black)
    toothmetal = Batch('Drivetrain | forty machined chainring teeth', silver)
    bolts = Batch('Drivetrain | recessed crank and chainring hardware', silver)
    recesses = Batch('Drivetrain | bolt recesses', black)

    def blade_outline(center, a, start, end, width0, width1, sweep=0):
        x,z=center
        # Unequal leading and trailing edges give the tapered GRX-style web.
        points=[]
        for r,w,t in [(start,-width0,0),(start+.015,-width0*.8,.15),
                      (end-.008,-width1,.8),(end,-width1*.5,1),
                      (end,width1*.5,1),(end-.008,width1,.8),
                      (start+.015,width0*.80,.15),(start,width0,0)]:
            aa=a+sweep*t
            points.append((x+r*cos(aa)-w*sin(aa),z+r*sin(aa)+w*cos(aa)))
        return points

    # A broad black outer ring and four visibly unequal, flat structural arms.
    dark.annulus((cx,cz), .0672, .0766, drive_y, .0047, 120)
    dark.annulus((cx,cz), .011, .027, drive_y-.0004, .008, 56)
    for k, a in enumerate([math.radians(64),math.radians(139),math.radians(254),math.radians(321)]):
        sweep=[.05,-.065,.075,-.045][k]
        dark.solid(blade_outline((cx,cz),a,.021,.073,.011,.0075,sweep),drive_y-.0004,.006)
        bx,bz=cx+.063*cos(a+sweep*.75),cz+.063*sin(a+sweep*.75)
        recesses.cylinder((bx,bz),.0057,drive_y-.0039,.0015,16)
        bolts.annulus((bx,bz),.0020,.0034,drive_y-.0048,.00065,16)
        recesses.cylinder((bx,bz),.0018,drive_y-.0053,.0008,6)
    # Teeth are integral flat plates with narrow valleys and squared tips.
    n=40*5
    outer=[(.0770 if i%5 in [0,4] else .0816 if i%5 in [2,3] else .0792) for i in range(n)]
    toothmetal.radial((cx,cz),[.0749]*n,outer,drive_y,.0020,pi/80)
    dark.finish();toothmetal.finish();bolts.finish();recesses.finish()

    # Sculpted broad-faced crank arms, with a chamfered rectangular cross section.
    crank_batch=Batch('Crank | hollow-profile sculpted arms',black)
    crank_trim=Batch('Crank | axle caps and pedal fixing hardware',silver)
    crank_dark=Batch('Crank | inset cap and pedal washers',black)
    def arm(side):
        dx,dz=.167,.048
        if side==1:dx,dz=-dx,-dz
        length=sqrt(dx*dx+dz*dz);ux,uz=dx/length,dz/length;vx,vz=-uz,ux
        # s, half width, center-Y, half depth. Face is on the exterior of each arm.
        sy=-1 if side==-1 else 1
        stations=[(-.014,.012,sy*.074,.007),(-.004,.020,sy*.078,.009),
                  (.029,.017,sy*.080,.010),(.080,.014,sy*.083,.009),
                  (.137,.0105,sy*.086,.008),(.164,.010,sy*.088,.007),
                  (length+.007,.0065,sy*.088,.006)]
        vv=[]
        for s,w,yy,h in stations:
            # Bevels are modelled, not a render-only modifier.
            for q,t in [(-w+.002,-h), (w-.002,-h),(w,-h+.002),(w,h-.002),
                        (w-.002,h),(-w+.002,h),(-w,h-.002),(-w,-h+.002)]:
                vv.append((cx+ux*s+vx*q,yy+t,cz+uz*s+vz*q))
        ff=[]
        for j in range(len(stations)-1):
            for k in range(8):ff.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
        ff+=[tuple(range(7,-1,-1)),tuple((len(stations)-1)*8+k for k in range(8))]
        crank_batch.add(vv,ff)
        crank_dark.cylinder((cx,cz),.0157,sy*.089,.0034,40)
        crank_trim.annulus((cx,cz),.0108,.0132,sy*.091,.0010,40)
        crank_dark.cylinder((cx,cz),.0101,sy*.092,.0010,32)
        ex,ez=cx+dx,cz+dz
        crank_trim.cylinder((ex,ez),.0056,sy*.106,.034,12)
        crank_dark.annulus((ex,ez),.0046,.0080,sy*.091,.0015,24)
        return ex,ez,sy
    ends=[arm(-1),arm(1)]
    crank_dark.cylinder((cx,cz),.012,0,.164,24)
    crank_batch.finish();crank_trim.finish();crank_dark.finish()
    # Small clipless pedals, not oversized blockout platforms.
    pedal_black=Batch('Pedal | compact SPD body and open retention base',black)
    pedal_steel=Batch('Pedal | silver retention jaws and spindle ends',silver)
    for ex,ez,sy in ends:
        py=sy*.120
        pedal_black.solid([(ex-.023,ez-.005),(ex-.018,ez-.011),(ex+.015,ez-.011),
                           (ex+.023,ez-.004),(ex+.020,ez+.008),(ex-.017,ez+.009)],py,.030)
        # Open silver hoops bound an actual center cleat opening.
        pedal_steel.annulus((ex,ez+.006),.0073,.010,py,.043,24)
        for j in [-1,1]:
            pedal_steel.solid([(ex+j*.014,ez-.003),(ex+j*.025,ez-.003),
                              (ex+j*.027,ez+.006),(ex+j*.020,ez+.014),
                              (ex+j*.014,ez+.010)],py,.042)
            pedal_black.cylinder((ex+j*.019,ez+.008),.0026,py,.044,8)
        pedal_steel.cylinder((ex,ez),.004,sy*.144,.003,12)
    pedal_black.finish();pedal_steel.finish()

    # Eleven actual pierced, flat sprockets on a shared splined freehub.
    cassette=Batch('Cassette | eleven stepped cutout sprockets',silver)
    cassette_dark=Batch('Cassette | spacers and carrier',black)
    counts=[40,35,32,28,25,22,19,17,15,13,11]
    cassette_y=[-.0312-j*.0040 for j in range(11)]
    pitch=.0127
    def gear(batch,center,count,y,thick,outer_extra=.0012,inner=None,spokes=5):
        pr=count*pitch/(2*pi)
        rr=pr+outer_extra
        base=pr-.0028
        nn=count*4
        tip=[base if i%4 in [0,3] else rr for i in range(nn)]
        inner=inner if inner is not None else max(.0105,pr-.0090)
        batch.radial(center,[inner]*nn,tip,y,thick,pi/(count*4))
        hub=.010 if pr<.029 else .0145
        batch.annulus(center,.0058,hub,y,thick,24)
        if inner>hub:
            for k in range(spokes):
                a=k*2*pi/spokes+.19
                batch.solid(blade_outline(center,a,hub-.002,inner+.002,
                                          .0020 if pr<.03 else .0037,
                                          .0019 if pr<.03 else .0032,.17),y,thick)
        return pr
    for j,count in enumerate(counts):
        gear(cassette,rear,count,cassette_y[j],.00135)
        if j<10:
            cassette_dark.annulus(rear,.008,.017 if j<6 else .012,cassette_y[j]-.002,.00225,16)
    cassette_dark.annulus(rear,.012,.027,-.0275,.0045,24)
    cassette.annulus(rear,.0065,.0142,-.0746,.0026,40)
    for j in range(12):
        a=2*pi*j/12
        cassette_dark.solid(blade_outline(rear,a,.010,.0138,.0006,.0006,0),-.0762,.0005)
    cassette.finish();cassette_dark.finish()

    # Hanger and articulated rear derailleur, mechanically joined to the dropout.
    body=Batch('Derailleur | hanger and angular parallelogram body',black)
    der_steel=Batch('Derailleur | pivot hardware and inner parallelogram',silver)
    body.solid([(-.536,.361),(-.517,.364),(-.505,.331),(-.512,.315),(-.532,.326)],-.078,.008)
    body.solid([(-.523,.330),(-.500,.327),(-.473,.296),(-.473,.278),(-.490,.276),(-.520,.302)],-.088,.020)
    body.solid([(-.494,.303),(-.473,.299),(-.453,.280),(-.456,.259),(-.478,.252),(-.492,.269)],-.076,.030)
    for a,b in [((-.517,.320),(-.484,.290)),((-.506,.329),(-.465,.286))]:
        ax,az=a;bx,bz=b;dd=Vector((bx-ax,0,bz-az)).normalized();nn=Vector((-dd.z,0,dd.x))*.003
        der_steel.solid([(ax+nn.x,az+nn.z),(bx+nn.x,bz+nn.z),(bx-nn.x,bz-nn.z),(ax-nn.x,az-nn.z)],-.100,.0022)
    for x,z,rr in [(-.524,.350,.006),(-.512,.320,.005),(-.481,.287,.0055),(-.463,.277,.0048)]:
        der_steel.annulus((x,z),rr*.44,rr,-.103,.002,18)
        body.cylinder((x,z),rr*.4,-.1045,.002,8)
    body.finish();der_steel.finish()

    guide=(-.474,.258);tension=(-.485,.168);pulley_y=-.058
    cage=Batch('Derailleur | paired thin open cage plates',black)
    pulleys=Batch('Derailleur | eleven-tooth open jockey wheels',black)
    pulhardware=Batch('Derailleur | cage axle and screw hardware',silver)
    # Two parallel flat cage plates, with an open center and a diagonal stiffener.
    p1,p2=Vector((guide[0],0,guide[1])),Vector((tension[0],0,tension[1]))
    dd=(p2-p1).normalized();normal=Vector((-dd.z,0,dd.x))
    for yy in [pulley_y-.0060,pulley_y+.0060]:
        for cc in [guide,tension]:cage.annulus(cc,.0180,.0250,yy,.0016,36)
        for side in [-1,1]:
            aa=p1+normal*(side*.019)+dd*.008
            bb=p2+normal*(side*.017)-dd*.008
            ww=.0034
            cage.solid([(aa.x+normal.x*ww,aa.z+normal.z*ww),
                        (bb.x+normal.x*ww,bb.z+normal.z*ww),
                        (bb.x-normal.x*ww,bb.z-normal.z*ww),
                        (aa.x-normal.x*ww,aa.z-normal.z*ww)],yy,.0016)
        # Thin diagonal brace leaves two elongated windows between pulley mounts.
        aa=p1.lerp(p2,.22)+normal*.016
        bb=p1.lerp(p2,.65)-normal*.016
        direction=(bb-aa).normalized();normal2=Vector((-direction.z,0,direction.x))*.0024
        cage.solid([(aa.x+normal2.x,aa.z+normal2.z),(bb.x+normal2.x,bb.z+normal2.z),
                    (bb.x-normal2.x,bb.z-normal2.z),(aa.x-normal2.x,aa.z-normal2.z)],yy,.0016)
    for cc in [guide,tension]:
        gear(pulleys,cc,11,pulley_y,.005,outer_extra=.0004,inner=.0144,spokes=5)
        pulhardware.cylinder(cc,.0037,pulley_y,.0170,12)
        pulhardware.annulus(cc,.002,.0055,pulley_y-.0075,.0014,20)
    cage.finish();pulleys.finish();pulhardware.finish()

    # Exact line/circle tangencies create a serpentine closed chain loop.
    # Sign +1: CCW contact; -1: clockwise contact on the upper guide wheel.
    selected=4
    circles=[(cx,cz,40*pitch/(2*pi),drive_y,1),
             (rear[0],rear[1],counts[selected]*pitch/(2*pi),cassette_y[selected],1),
             (guide[0],guide[1],11*pitch/(2*pi),pulley_y,-1),
             (tension[0],tension[1],11*pitch/(2*pi),pulley_y,1)]
    tangent=[]
    for i,cc in enumerate(circles):
        jj=circles[(i+1)%len(circles)]
        x,z,r,y,s=cc;xx,zz,rr,yy,ss=jj
        dx,dz=xx-x,zz-z;length=sqrt(dx*dx+dz*dz)
        theta=atan2(dz,dx)-math.asin((rr*ss-r*s)/length)
        nx,nz=-sin(theta),cos(theta)
        aa=Vector((x-r*s*nx,y,z-r*s*nz))
        bb=Vector((xx-rr*ss*nx,yy,zz-rr*ss*nz))
        tangent.append((aa,bb))
    dense=[]
    for i,cc in enumerate(circles):
        x,z,r,y,sign=cc
        incoming=tangent[(i-1)%4][1];outgoing=tangent[i][0]
        a=atan2(incoming.z-z,incoming.x-x);b=atan2(outgoing.z-z,outgoing.x-x)
        delta=(b-a)%(2*pi) if sign>0 else -((a-b)%(2*pi))
        steps=max(12,int(abs(delta)*r/.0014))
        for j in range(steps):
            angle=a+delta*j/steps;dense.append(Vector((x+r*cos(angle),y,z+r*sin(angle))))
        aa,bb=tangent[i]
        steps=max(2,int((bb-aa).length/.0014))
        for j in range(steps):dense.append(aa.lerp(bb,j/steps))
    dense.append(dense[0])
    distances=[0.]
    for a,b in zip(dense[:-1],dense[1:]):distances.append(distances[-1]+(b-a).length)
    total=distances[-1];links=int(round(total/pitch/2))*2;step=total/links
    points=[];j=0
    for k in range(links):
        distance=k*step
        while distances[j+1]<distance:j+=1
        t=(distance-distances[j])/(distances[j+1]-distances[j])
        points.append(dense[j].lerp(dense[j+1],t))
    plates=Batch('Chain | alternating inner and outer figure-eight link plates',chainmat)
    rollers=Batch('Chain | separate barrel rollers',black)
    pins=Batch('Chain | exposed rivets and brushed roller ends',silver)
    for k,aa in enumerate(points):
        bb=points[(k+1)%links];mid=(aa+bb)/2
        # Local axes are fitted to each pair of roller centers, including chainline skew.
        direction=(bb-aa).normalized();across=Vector((0,1,0));up=direction.cross(across).normalized()
        across=up.cross(direction).normalized()
        half=(bb-aa).length/2;r=.00325
        outline=[]
        for q in range(5):
            a=pi/2+pi*q/4;outline.append((-half+r*cos(a),r*sin(a)))
        outline.append((0,-.0020))
        for q in range(5):
            a=-pi/2+pi*q/4;outline.append((half+r*cos(a),r*sin(a)))
        outline.append((0,.0020))
        lateral=.00350 if k%2==0 else .00248
        for sign in [-1,1]:
            vv=[];thick=.00064;n=len(outline)
            for off in [-thick/2,thick/2]:
                for xx,zz in outline:vv.append(tuple(mid+direction*xx+up*zz+across*(sign*lateral+off)))
            poly=[Vector((x,0,z)) for x,z in outline]
            lookup={tuple(v):i for i,v in enumerate(poly)}
            ff=[]
            for tri in tessellate_polygon([poly]):
                ids=[v if isinstance(v, int) else lookup[tuple(v)] for v in tri]
                ff.extend([tuple(reversed(ids)),tuple(i+n for i in ids)])
            ff.extend((q,(q+1)%n,(q+1)%n+n,q+n) for q in range(n))
            plates.add(vv,ff)
        rollers.cylinder((aa.x,aa.z),.0028,aa.y,.0047,8)
        pins.cylinder((aa.x,aa.z),.00148,aa.y,.0083,8)
    plateob=plates.finish();rollers.finish();pins.finish()
    plateob['link_count']=links
    plateob['nominal_pitch_m']=pitch
    plateob['resampled_pitch_m']=step
    plateob['path']='Circle tangencies around 40T chainring, selected 25T cassette, 11T guide and tension pulleys'

    # Thin slotted disc rotors with six broad planar arms and real paired calipers.
    for name,cc,theta in [('Front',front,3*pi/4),('Rear',rear,pi/4)]:
        rotor=Batch('Brake_'+name+' | flat slotted 160 mm rotor',silver)
        spider=Batch('Brake_'+name+' | rotor carrier and caliper brackets',black)
        by=.044;xx,zz=cc
        # Two steel tracks connected by short radial bridges create eighteen open slots.
        rotor.annulus(cc,.0766,.0800,by,.00155,96)
        rotor.annulus(cc,.0663,.0701,by,.00155,96)
        for j in range(18):
            a=j*2*pi/18;span=.092
            rotor.solid([(xx+r*cos(aa),zz+r*sin(aa)) for r,aa in
                         [(.0696,a-span),(.0770,a-span+.025),(.0770,a+span),(.0696,a+span-.025)]],by,.00155)
        rotor.annulus(cc,.0120,.0230,by,.0018,48)
        for j in range(6):
            a=j*pi/3
            rotor.solid(blade_outline(cc,a,.020,.0677,.0045,.0045,.24),by,.00155)
            rotor.cylinder((xx+.017*cos(a),zz+.017*sin(a)),.0025,by+.0017,.0020,10)
            spider.cylinder((xx+.017*cos(a),zz+.017*sin(a)),.0015,by+.003,.001,6)
        spider.annulus(cc,.009,.0132,by,.003,36)
        # Mount the caliper around the rotor at the adjacent fork/stay, not in empty space.
        radial=Vector((cos(theta),0,sin(theta)))
        tangentv=Vector((-sin(theta),0,cos(theta)))
        center=Vector((xx,0,zz))+radial*.076
        def calpoly(rad0,rad1,tan0,tan1):
            return [(center.x+radial.x*r+tangentv.x*t,center.z+radial.z*r+tangentv.z*t)
                    for r,t in [(rad0,tan0),(rad1,tan0),(rad1,tan1),(rad0,tan1)]]
        caliper=Batch('Brake_'+name+' | hydraulic caliper body and bridge',black)
        calmetal=Batch('Brake_'+name+' | caliper mount bolts and pad backs',silver)
        # Pads sit on each side of the rotor; bridge is just outside its outer edge.
        caliper.solid(calpoly(-.012,.009,-.020,.020),.055,.016)
        caliper.solid(calpoly(-.011,.009,-.018,.018),.0335,.011)
        caliper.solid(calpoly(.004,.013,-.019,.019),.044,.027)
        calmetal.solid(calpoly(-.011,.002,-.015,.015),.0459,.0008)
        calmetal.solid(calpoly(-.011,.002,-.015,.015),.0421,.0008)
        # Flat mounting adapter reaches the physical fork / rear seatstay.
        mount=calpoly(-.019,-.010,-.032,.032)
        spider.solid(mount,.054,.010)
        for tt in [-.025,.025]:
            bp=center+radial*(-.013)+tangentv*tt
            calmetal.cylinder((bp.x,bp.z),.0036,.063,.007,12)
            spider.cylinder((bp.x,bp.z),.0017,.067,.0012,6)
        # Bleed nipple and hose socket give a readable hydraulic-caliper silhouette.
        nipple=center+tangentv*.020
        calmetal.cylinder((nipple.x,nipple.z),.0030,.061,.009,10)
        caliper.cylinder((nipple.x,nipple.z),.0041,.066,.004,10)
        rotor.finish();spider.finish();caliper.finish();calmetal.finish()

    # Discreet white GRX lettering is visible on the reference crank.
    labelmat=bpy.data.materials.get('Crank | warm white logo')
    if labelmat is None:
        labelmat=bpy.data.materials.new('Crank | warm white logo')
        labelmat.diffuse_color=(.77,.79,.78,1)
        labelmat.use_nodes=True
        bs=labelmat.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value=(.77,.79,.78,1)
        bs.inputs['Roughness'].default_value=.45
    font=bpy.data.curves.new('Crank GRX lettering','FONT');font.body='GRX';font.size=.0115
    font.align_x='CENTER';font.align_y='CENTER';font.extrude=.00002; font.resolution_u=3
    textob=bpy.data.objects.new('Crank | GRX face lettering',font)
    root.users_collection[0].objects.link(textob);textob.parent=root
    angle=atan2(.048,.167);ux=Vector((cos(angle),0,sin(angle)));uy=Vector((-sin(angle),0,cos(angle)));uz=Vector((0,-1,0))
    textob.matrix_world=Matrix(((ux.x,uy.x,uz.x,0),(ux.y,uy.y,uz.y,0),(ux.z,uy.z,uz.z,0),(0,0,0,1)))
    textob.location=(cx+.082*cos(angle),-.09265,cz+.082*sin(angle))
    font.materials.append(labelmat)
    bpy.context.view_layer.objects.active=textob;textob.select_set(True)
    bpy.ops.object.convert(target='MESH');textob.select_set(False)
    created.append(textob)
    for ob in created:ob['refinement']='Photo-informed mechanics v2; counts and dimensions inferred'
    triangles=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in created if ob.type=='MESH')
    return {'objects':created,'triangles':triangles,'chain_links':links,'chain_length_m':total,
            'cassette_teeth':counts,'selected_cog_teeth':counts[selected]}
