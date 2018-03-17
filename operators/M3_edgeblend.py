import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty
import bmesh
from .. import M3utils as m3
import math
import mathutils


class LoopMachine(bpy.types.Operator):
    bl_idname = "machin3.loop_machine"
    bl_label = "MACHIN3: Loop Machine"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = m3.get_active()
        mesh = active.data

        m3.set_mode("OBJECT")

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.normal_update()

        bVerts = bm.verts
        bEdges = bm.edges
        bFaces = bm.faces

        # verts = [v for v in bVerts if v.select]
        edges = [e for e in bEdges if e.select]
        # faces = [f for f in bFaces if f.select]

        m3.clear()

        # initialize dictionary
        seldict = {}
        # for e in edges[0:1]:
        for e in edges:
            seldict[e] = {}
            for vert in e.verts:
                seldict[e][vert] = {}
                seldict[e][vert]["connected"] = []
                seldict[e][vert]["loop"] = None
                for edge in vert.link_edges:
                    if edge != e and edge not in seldict[e][vert]["connected"]:
                        seldict[e][vert]["connected"].append(edge)

        for edge in seldict:
            print("edge:", edge)
            for vert in seldict[edge]:
                print(" » vert:", vert)
                for e in seldict[edge][vert]["connected"]:
                    print("   » edge:", e)
                print("   » loop:", seldict[edge][vert]["loop"])

        print()

        for edge in seldict:
            for vert in seldict[edge]:
                if len(seldict[edge][vert]["connected"]) >= 3:
                    loop = self.simple_loop(seldict, edge, vert)
                    seldict[edge][vert]["loop"] = loop
                    loop.select = True
                elif len(seldict[edge][vert]["connected"]) == 2:
                    ngon = self.check_ngon(edge)
                    if ngon:
                        loop = self.ngon_loop(ngon, edge, vert)
                        seldict[edge][vert]["loop"] = loop
                        loop.select = True
                    else:
                        print("magic loop")
                        loop = self.magic_loop(bm, edge, vert, seldict[edge][vert]["connected"])
                        seldict[edge][vert]["loop"] = loop
                        loop.select = True

                        # angle = self.check_angle(seldict[edge][vert]["connected"])
                        # if angle < 180:
                            # print("angle loop")
                            # loop = self.angle_loop(bm, vert, seldict[edge][vert]["connected"])
                            # seldict[edge][vert]["loop"] = loop
                            # loop.select = True
                            # print("magic loop")
                            # loop = self.magic_loop(bm, edge, vert, seldict[edge][vert]["connected"])
                        # else:
                            # print("magic loop")
                            # loop = self.magic_loop(bm, edge, vert, seldict[edge][vert]["connected"])
                else:
                    print("undecided")

        for edge in seldict:
            print("edge:", edge)
            for vert in seldict[edge]:
                print(" » vert:", vert)
                print("   » edges:")
                for e in seldict[edge][vert]["connected"]:
                    print("     »", e)
                print("   » loop:", seldict[edge][vert]["loop"])

        bm.to_mesh(mesh)

        m3.set_mode("EDIT")

        return {'FINISHED'}

    def magic_loop(self, bm, edge, vert, connected, debug=False):
        # get the face, that's not bordering the center edge
        edgefaces = [f for f in edge.link_faces]

        for loop in vert.link_loops:
            if loop.face not in edgefaces:
                face = loop.face

        # the 2 faces bordering the center edge
        f1 = edgefaces[0]
        f2 = edgefaces[1]

        # face median centers
        m1co = f1.calc_center_median()  # NOTE: there's also calc_center_median_weighted()
        m2co = f2.calc_center_median()

        if debug:
            m1 = bm.verts.new()
            m1.co = m1co

            m2 = bm.verts.new()
            m2.co = m2co

        # points where face normals intersect the face not bordering the center edge
        i1co = mathutils.geometry.intersect_line_plane(m1co, m1co + f1.normal, vert.co, face.normal)
        i2co = mathutils.geometry.intersect_line_plane(m2co, m2co + f2.normal, vert.co, face.normal)

        if debug:
            i1 = bm.verts.new()
            i1.co = i1co

            i2 = bm.verts.new()
            i2.co = i2co

            i1edge = bm.edges.new((m1, i1))
            i2edge = bm.edges.new((m2, i2))

        # projecting the intersection points across the centeredge endpoint vert
        crossv1co = vert.co + (vert.co - i1co)
        crossv2co = vert.co + (vert.co - i2co)

        if debug:
            crossv1 = bm.verts.new()
            crossv1.co = crossv1co

            crossv2 = bm.verts.new()
            crossv2.co = crossv2co

            cross1edge = bm.edges.new((crossv1, i1))
            cross2edge = bm.edges.new((crossv2, i2))

            crossedge = bm.edges.new((crossv1, crossv2))

        # point orthogonal to the crossedge in the direction of the vert( == the closest point on that vector to the end point vert)
        crossvco, distance = mathutils.geometry.intersect_point_line(vert.co, crossv1co, crossv2co)

        crossv = bm.verts.new()
        crossv.co = crossvco

        loop = bm.edges.new((vert, crossv))

        return loop

    def angle_loop(self, bm, vert, connected):
        vert1 = connected[0].other_vert(vert)
        vert2 = connected[1].other_vert(vert)

        v = bm.verts.new()
        v.co = vert1.co + (vert2.co - vert1.co) * 0.5

        e = bm.edges.new((vert, v))

        return e

    def check_angle(self, edges):
        angle = get_angle_between_edges(edges[0], edges[1], radians=False)
        return angle

    def ngon_loop(self, ngon, edge, vert):
        for e in ngon.edges:
            if e != edge and vert in e.verts:
                print("ngon loop")
                return e

    def check_ngon(self, edge):
        for f in edge.link_faces:
            if len(f.verts) > 4:
                return f
        return False

    def simple_loop(self, seldict, edge, vert):
        connected = seldict[edge][vert]["connected"]

        # exclude the edges that share a face with the selected edge
        exclude = []
        for loop in edge.link_loops:
            l1 = loop.link_loop_next
            l2 = loop.link_loop_prev

            if l1.edge in connected:
                exclude.append(l1.edge)
            if l2.edge in connected:
                exclude.append(l2.edge)

        edges = list(set(connected) - set(exclude))

        if len(edges) == 1:  # standard behaviour
            print("simple loop")
            return edges[0]
        else:  # take the edge with the biggest angle  to the center edge
            angle = 0
            for e in edges:
                a = get_angle_between_edges(edge, e, radians=False)
                if a > angle:
                    angle = a
                    loop = e
            print("simple loop, biggest angle")
            return loop


class LoopMan(bpy.types.Operator):
    bl_idname = "machin3.loop_man"
    bl_label = "MACHIN3: LoopMan"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = m3.get_active()
        mesh = active.data

        m3.set_mode("OBJECT")

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.normal_update()

        bVerts = bm.verts
        bEdges = bm.edges
        bFaces = bm.faces

        verts = [v for v in bVerts if v.select]
        edges = [e for e in bEdges if e.select]
        faces = [f for f in bFaces if f.select]

        m3.clear()

        e = edges[0]

        # get egdes connects to the selected edge
        connected_edges = []
        for vert in e.verts:
            for edge in vert.link_edges:
                if edge != e and edge not in connected_edges:
                    connected_edges.append(edge)

        # remove the edges that share a face with the selected edge
        for loop in e.link_loops:
            connected_edges.remove(loop.link_loop_next.edge)
            connected_edges.remove(loop.link_loop_prev.edge)

        for edge in connected_edges:
            edge.select = True

        # l = e.link_loops[0]

        # p = l.link_loop_prev.edge
        # n = l.link_loop_next.edge
        # # p = l.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge
        # # n = l.link_loop_next.link_loop_radial_prev.link_loop_next.edge

        # p.select = True
        # n.select = True


        # loop = loop.link_loop_prev.link_loop_radial_prev.link_loop_prev

        bm.to_mesh(mesh)

        m3.set_mode("EDIT")

        return {'FINISHED'}


class AngleMan(bpy.types.Operator):
    bl_idname = "machin3.angle_man"
    bl_label = "MACHIN3: AngleMan"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = m3.get_active()
        mesh = active.data

        m3.set_mode("OBJECT")

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.normal_update()

        bEdges = bm.edges
        bVerts = bm.verts

        edges = [e for e in bEdges if e.select]

        e1 = edges[0]
        e2 = edges[1]

        # angle = get_angle_between_edges(e1, e2)
        # print(angle)

        angle = get_angle_between_edges(e1, e2, radians=False)
        print(angle)

        bm.to_mesh(mesh)

        m3.set_mode("EDIT")

        return {'FINISHED'}


class EdgeBlend(bpy.types.Operator):
    bl_idname = "machin3.edge_blend"
    bl_label = "MACHIN3: Edge Blend"
    bl_options = {'REGISTER', 'UNDO'}

    segments = IntProperty(name="Segments", default=6, min=0, max=30)

    strength = FloatProperty(name="Strength", default=1, min=0, max=2)

    cyclic = BoolProperty(name="Cyclic", default=False)
    capholes = BoolProperty(name="Cap Holes", default=False)
    captolerance = FloatProperty(name="Tolerance", default=0.01, min=0, max=0.2, precision=4, step=0.01)
    flip = BoolProperty(name="Flip", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "segments")
        column.prop(self, "strength")

        column.prop(self, "cyclic")

        row = column.row()
        row.prop(self, "capholes")
        row.prop(self, "captolerance")

        column.prop(self, "flip")

    def execute(self, context):
        active = m3.get_active()
        mesh = active.data

        mode = m3.get_mode()

        if mode == "EDGE":
            m3.set_mode("FACE")

        # get the initial face, edge and vert selection
        m3.set_mode("OBJECT")
        selectedfaces = [face.index for face in mesh.polygons if face.select]
        selectededges = [edge.index for edge in mesh.edges if edge.select]
        selectedverts = [vert.index for vert in mesh.vertices if vert.select]
        m3.set_mode("EDIT")

        # get the ring edges
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')
        bpy.ops.mesh.loop_multi_select(ring=True)

        m3.set_mode("OBJECT")
        ringedges = [edge.index for edge in mesh.edges if edge.select]

        # check them against the initially selected edges and only leave the center edges
        centeredges = []
        for edge in ringedges:
            if edge not in selectededges:
                mesh.edges[edge].select = False
            else:
                centeredges.append(edge)

        m3.set_mode("EDIT")

        # loop the center edges, then unselect the edges that aren't touching the initial selection
        bpy.ops.mesh.loop_multi_select(ring=False)

        m3.set_mode("OBJECT")
        loopedges = [edge.index for edge in mesh.edges if edge.select]

        railedges = []
        for edge in loopedges:
            if any([vert for vert in mesh.edges[edge].vertices if vert in selectedverts]):
                railedges.append(edge)
            else:
                mesh.edges[edge].select = False

        # if, as a result of the loop a face "is selected", as happens at the end of a prismatic mesh, the face fill won't update propertly if you unselect loop edges not beloing to the rail
        # it works if i force it like so and then just reselect the rail edges again
        # this is related i thinK:
        # Note
        # Currently this only flushes down, so selecting a face will select all its vertices but de-selecting a vertex won’t de-select all the faces that use it, before finishing with a mesh typically flushing is still needed.
        # https://docs.blender.org/api/current/bmesh.types.html#bmesh.types.BMVert.select_set
        # m3.set_mode("EDIT")
        # m3.unselect_all("MESH")

        # m3.set_mode("OBJECT")
        # for edge in railedges:
            # mesh.edges[edge].select =True
        # m3.set_mode("EDIT")

        # BMESH /////////////////////////////////////////////

        m3.set_mode("OBJECT")

        dup = active.copy()
        dup.data = active.data.copy()
        bpy.context.scene.objects.link(dup)
        m3.make_active(dup)

        dup.name = "BMESH"
        active.hide = True

        bm = bmesh.new()
        bm.from_mesh(dup.data)
        bm.normal_update()

        # remove everything but the rail edges

        rm = [e for e in bm.edges if e.index not in railedges]
        bmesh.ops.delete(bm, geom=rm, context=2)

        bEdges = bm.edges
        bVerts = bm.verts

        allverts = [v for v in bVerts]

        rails = get_rails(allverts)

        handles = create_handles(bVerts, rails, self.strength)

        splines = create_splines(bVerts, bEdges, handles, self.segments)

        # remove original center edges
        rm = [r[1] for r in rails]

        # context enum: see https://blender.stackexchange.com/a/1542/33919
        # 1: DEL_VERTS, 2: DEL_EDGES, 3: DEL_ONLYFACES, 4: DEL_EDGESFACES, 5: DEL_FACES, 6: DEL_ALL, 7: DEL_ONLYTAGGED};
        bmesh.ops.delete(bm, geom=rm, context=2)

        splineedges = []
        for verts, edges in splines:
            splineedges += edges

        if splineedges:
            bmesh.ops.bridge_loops(bm, edges=splineedges, use_cyclic=self.cyclic)
            # NOTE: this op actually returns the faces it creates!

        bm.to_mesh(dup.data)

        # /BMESH /////////////////////////////////////////////

        active.hide = False
        active.select = True
        m3.make_active(active)

        if splineedges:
            bpy.ops.object.join()
        else:
            bpy.data.objects.remove(dup, do_unlink=True)

        m3.set_mode("EDIT")
        m3.set_mode("FACE")

        if splineedges:
            m3.select_all("MESH")
            bpy.ops.mesh.remove_doubles()

        m3.unselect_all("MESH")

        # delete the initially selected faces
        m3.set_mode("OBJECT")
        for face in selectedfaces:
            mesh.polygons[face].select = True

        m3.set_mode("EDIT")

        if splineedges:
            bpy.ops.mesh.delete(type='FACE')

        m3.select_all("MESH")
        bpy.ops.mesh.normals_make_consistent(inside=False)

        if self.flip:
            bpy.ops.mesh.flip_normals()
        m3.unselect_all("MESH")

        if splineedges and self.capholes:
            m3.set_mode("EDGE")
            bpy.ops.mesh.select_non_manifold()
            bpy.ops.mesh.edge_face_add()
            m3.set_mode("FACE")

            bpy.ops.mesh.select_similar(type='COPLANAR', threshold=self.captolerance)
            bpy.ops.mesh.dissolve_mode()

            m3.unselect_all("MESH")

        if not splineedges:
            m3.set_mode("OBJECT")
            for face in selectedfaces:
                mesh.polygons[face].select = True

            m3.set_mode("EDIT")

        return {'FINISHED'}


def create_splines(bVerts, bEdges, handles, segments):
    splines = []
    for h in handles:
        end1 = h[0][0]
        handle1 = h[0][1]

        end2 = h[1][0]
        handle2 = h[1][1]

        bezierverts = mathutils.geometry.interpolate_bezier(end1.co, handle1, handle2, end2.co, segments + 2)[1:-1]

        splineverts = []

        splineverts.append(end1)
        for vert in bezierverts:
            v = bVerts.new()
            v.co = vert
            splineverts.append(v)
        splineverts.append(end2)

        splineedges = []
        for idx, vert in enumerate(splineverts):
            if idx == len(splineverts) - 1:
                break
            else:
                try:
                    e = bEdges.new((vert, splineverts[idx + 1]))
                    splineedges.append(e)
                except:
                    pass


        splines.append((splineverts, splineedges))

    return splines


def create_handles(bVerts, rails, strength):
    handles = []
    for rail in rails:
        rail1 = rail[0]
        rail2 = rail[2]

        vA1, vA2 = rail1.verts
        vB1, vB2 = rail2.verts

        # tuple, the first item is the handle for the first rail, the second for the second
        h = mathutils.geometry.intersect_line_line(vA1.co, vA2.co, vB1.co, vB2.co)

        # find endpoints, the verts positioned towards the handles
        # or rathter the verts connected to 2 edges
        for vert in rail1.verts:
            if len(vert.link_edges) == 2:
                end1 = vert

        for vert in rail2.verts:
            if len(vert.link_edges) == 2:
                end2 = vert

        # take the handles and and add in the strength
        handle1 = end1.co + ((h[0] - end1.co) * strength)
        handle2 = end2.co + ((h[1] - end2.co) * strength)

        handles.append(((end1, handle1), (end2, handle2)))

    return handles


def get_rails(allverts):
    rails = []

    while allverts:
        # take the first vert
        vert = allverts[0]
        edges = []

        # append all edges of that vert(1 or 2) to an edge list
        for edge in vert.link_edges:
            edges.append(edge)

        # keep adding edges connected to the verts of the edges in the edge list, until the list has 3 edges, which is a complete rail
        while len(edges) < 3:
            for edge in edges:
                for vert in edge.verts:
                    for e in vert.link_edges:
                        if e not in edges:
                            edges.append(e)

        # remove the verts of the rail form the list of all verts, so in the next iteration there's a fresh new vert
        for edge in edges:
            for vert in edge.verts:
                if vert in allverts:
                    allverts.remove(vert)

        rails.append(edges)

    # put the center edge in the middle
    for rail in rails:
        for edge in rail:
            if len(edge.verts[0].link_edges) == 2:
                if len(edge.verts[1].link_edges) == 2:
                    idx = rail.index(edge)
                    if idx != 1:
                        rail.insert(1, rail.pop(idx))
                    break

    return rails


def get_angle_between_edges(edge1, edge2, radians=True):
    # check if edges share a vert, in which case we can properly set up the vectors and get a reliable angle
    # otherwise and angle could be either 2 or 178 depending on vert ids/order
    centervert = None
    for vert in edge1.verts:
        if vert in edge2.verts:
            centervert = vert

    if centervert:
        vector1 = centervert.co - edge1.other_vert(centervert).co
        vector2 = centervert.co - edge2.other_vert(centervert).co
    else:
        vector1 = edge1.verts[0].co - edge1.verts[1].co
        vector2 = edge2.verts[0].co - edge2.verts[1].co

    if radians:
        return vector1.angle(vector2)
    else:
        return math.degrees(vector1.angle(vector2))


def get_distance_between_verts(vert1, vert2, getvectorlength=True):
    if getvectorlength:
        vector = vert1.co - vert2.co
        return vector.length
    else:
        return math.sqrt((vert1.co[0] - vert2.co[0]) ** 2 + (vert1.co[1] - vert2.co[1]) ** 2 + (vert1.co[2] - vert2.co[2]) ** 2)
