import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty
import bmesh
from .. import M3utils as m3
import math
import mathutils

#TODO: force magic loop option, even for simple loops?
#TODO: tri based center vert movement?


class Fuse(bpy.types.Operator):
    bl_idname = "machin3.fuse"
    bl_label = "MACHIN3: Fuse"
    bl_options = {'REGISTER', 'UNDO'}

    segments = IntProperty(name="Segments", default=6, min=0, max=30)
    tension = FloatProperty(name="Tension", default=1, min=0.01, max=2)
    # tension = FloatProperty(name="Tension", default=0.7, min=0.01, max=2)

    strict = BoolProperty(name="Strict", default=True)

    cyclic = BoolProperty(name="Cyclic", default=False)
    # capholes = BoolProperty(name="Cap Holes", default=False)
    # captolerance = FloatProperty(name="Tolerance", default=0.01, min=0, max=0.2, precision=4, step=0.01)
    # flip = BoolProperty(name="Flip", default=False)

    def execute(self, context):
        active = m3.get_active()
        mesh = active.data

        mode = m3.get_mode()
        if mode != "FACE":
            m3.set_mode("FACE")

        m3.set_mode("OBJECT")

        # get ring edges from polygon selection
        ringedgeids, selfaceids = self.get_ring_edges(mesh)

        # create bmesh
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.normal_update()

        edges = [e for e in bm.edges if e.index in ringedgeids]

        # get ring edges, create dict adn find/create rails
        if edges:
            seldict = self.init_dict(edges)
            self.create_rails(bm, seldict, debug=False)
            self.create_handles(bm, seldict, debug=False)
            # self.debug_dict(seldict)

            splineedges = self.create_splines(bm, seldict)

            # remove edges created by magic loop and the originally selected faces
            self.clean_up(bm, seldict, selfaceids, magicloop=True, initialfaces=True)

            if splineedges:
                # NOTE: this op actually returns the faces it creates!
                bmesh.ops.bridge_loops(bm, edges=splineedges, use_cyclic=self.cyclic)

        bm.to_mesh(mesh)
        m3.set_mode("EDIT")
        m3.set_mode(mode)

        # m3.set_mode("FACE")
        # m3.set_mode("EDGE")
        # m3.set_mode("VERT")

        self.finalize_mesh()

        return {'FINISHED'}

    def finalize_mesh(self):
        m3.select_all("MESH")
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)
        m3.unselect_all("MESH")

    def clean_up(self, bm, seldict, selfaceids, magicloop=True, initialfaces=True):
        # remove the magic loops
        if magicloop:
            magicloops = []
            for edge in seldict:
                for vert in seldict[edge]:
                    if seldict[edge][vert]["magicloop"]:
                        magicloops.append(seldict[edge][vert]["loop"])

            # 1: DEL_VERTS, 2: DEL_EDGES, 3: DEL_ONLYFACES, 4: DEL_EDGESFACES, 5: DEL_FACES, 6: DEL_ALL, 7: DEL_ONLYTAGGED};
            # see https://blender.stackexchange.com/a/1542/33919 for context enum details
            bmesh.ops.delete(bm, geom=magicloops, context=2)

        if initialfaces:
            # remove originally selected faces
            if self.segments > 0:
                faces = [f for f in bm.faces if f.index in selfaceids]
                bmesh.ops.delete(bm, geom=faces, context=5)

    def create_splines(self, bm, seldict):
        splineedges = []

        for edge in seldict:
            verts = []
            handles= []
            for vert in seldict[edge]:
                verts.append(vert)
                handles.append(seldict[edge][vert]["handle"])

            bezierverts = mathutils.geometry.interpolate_bezier(verts[0].co, handles[0], handles[1], verts[1].co, self.segments + 2)[1:-1]

            splineverts = []
            splineverts.append(verts[0])
            for vert in bezierverts:
                v = bm.verts.new()
                v.co = vert
                splineverts.append(v)
            splineverts.append(verts[1])

            if self.segments > 0:
                for idx, vert in enumerate(splineverts):
                    if idx == len(splineverts) - 1:
                        break
                    else:
                        e = bm.edges.new((vert, splineverts[idx + 1]))
                        splineedges.append(e)

        return splineedges

    def create_handles(self, bm, seldict, debug=False):
        for edge in seldict:
            loops = []
            verts = []
            for vert in seldict[edge]:
                verts.append(vert)
                loops.append(seldict[edge][vert]["loop"])

            # vA1, vA2 = loops[0].verts
            # vB1, vB2 = loops[1].verts
            end1 = verts[0]
            loopend1 = loops[0].other_vert(end1)

            end2 = verts[1]
            loopend2 = loops[1].other_vert(end2)

            # distance between both endpoints
            enddist = get_distance_between_points(end1.co, end2.co)

            # directions of loop edges
            dir1 = end1.co - loopend1.co
            dir2 = end2.co - loopend2.co

            # tuple, the first item is the handle for the first edge, the second for the other
            h = mathutils.geometry.intersect_line_line(end1.co, loopend1.co, end2.co, loopend2.co)

            if h is None:  # if the edge and both loop egdes are on the same line or are parallel: _._._ or  _./'¯¯
                h1 = (end1.co + dir1.normalized() * enddist / 2)
                h2 = (end2.co + dir2.normalized() * enddist / 2)

                h = (h1, h2)

                if debug:
                    print("handles could not be determined via line-line instersection, falling back to aligned center handles")

            # in an edge case like this:  _._./  the handle of the right loop edge will be in the same location as the end vert
            # this will result in an exception when trying to determine the angle between the handles (dirangle), so push that handle out by half the distance of the end points
            if end1.co == h[0] or end2.co == h[1]:
                h1 = (end1.co + dir1.normalized() * enddist / 2)
                h2 = (end2.co + dir2.normalized() * enddist / 2)

                h = (h1, h2)
                if debug:
                    print("handle position lies on end point, created aligned center handles instead")

            # take the handles and add in the tension
            handle1 = end1.co + ((h[0] - end1.co) * self.tension)
            handle2 = end2.co + ((h[1] - end2.co) * self.tension)

            # check if the handle is going into the right direction, which is the direction of the loop edges, towards the center edge
            handledir1 = handle1 - end1.co
            handledir2 = handle2 - end2.co

            dot1 = dir1.dot(handledir1)
            dot2 = dir2.dot(handledir2)

            # if necessary, create a new handle with the same length, but the propper direction
            if dot1 < 0:
                handle1 = end1.co + dir1.normalized() * handledir1.length
                handledir1 = handle1 - end1.co

                if debug:
                    print("flipped handle direction")

            if dot2 < 0:
                handle2 = end2.co + dir2.normalized() * handledir2.length
                handledir2 = handle2 - end2.co
                if debug:
                    print("flipped handle direction")

            # check handle length and correct if necessary
            # the length ratio should never be above 1 for a tension of 1, in ideal cases it sits around 0.7 if the surface angle is 90 degrees
            # it looks like the ideal ratio is tension / dirangle (radians)
            # a good max ratio seems to be ideal ratio + tension

            dist1 = get_distance_between_points(end1.co, handle1)
            dist2 = get_distance_between_points(end2.co, handle2)

            ratio1 = dist1 / enddist
            ratio2 = dist2 / enddist

            dirangle = handledir1.angle(handledir2)

            ratioideal = self.tension / dirangle
            ratiomax = self.tension + ratioideal

            if ratio1 > ratiomax or ratio2 > ratiomax:
                if debug:
                    print("surface angle:", math.degrees(dirangle), dirangle)
                    print("ideal ratio:", ratioideal, "max ratio:", ratiomax)

                if ratio1 > ratiomax:
                    handle1 = end1.co + dir1.normalized() * enddist * ratioideal * self.tension
                    if debug:
                        print("actual ratio:", ratio1)
                        print("corrected handle overshoot")

                if ratio2 > ratiomax:
                    handle2 = end2.co + dir2.normalized() * enddist * ratioideal * self.tension
                    if debug:
                        print("actual ratio:", ratio2)
                        print("corrected handle overshoot")

            seldict[edge][verts[0]]["handle"] = handle1
            seldict[edge][verts[1]]["handle"] = handle2

            if debug:
                v1 = bm.verts.new()
                v1.co = handle1

                v2 = bm.verts.new()
                v2.co = handle2

                bm.edges.new((end1, v1))
                bm.edges.new((end2, v2))

    def create_rails(self, bm, seldict, debug=False):
        # find/create loop edges
        for edge in seldict:
            for vert in seldict[edge]:
                if len(seldict[edge][vert]["connected"]) >= 3:
                    loop = self.simple_loop(seldict, edge, vert, debug=debug)
                elif len(seldict[edge][vert]["connected"]) == 2:
                    ngon = self.check_ngon(edge)
                    if ngon:
                        loop = self.ngon_loop(ngon, edge, vert, debug=debug)
                    else:
                        loop = self.magic_loop(bm, edge, vert, seldict[edge][vert]["connected"], debug=debug)
                        seldict[edge][vert]["magicloop"] = True

                seldict[edge][vert]["loop"] = loop
                if debug:
                    loop.select = True

    def init_dict(self, edges):
        # initialize dictionary
        seldict = {}
        for e in edges:
            seldict[e] = {}
            for vert in e.verts:
                seldict[e][vert] = {}
                seldict[e][vert]["connected"] = []
                seldict[e][vert]["loop"] = None
                seldict[e][vert]["magicloop"] = False
                seldict[e][vert]["handle"] = None
                for edge in vert.link_edges:
                    if edge != e and edge not in seldict[e][vert]["connected"]:
                        seldict[e][vert]["connected"].append(edge)
        return seldict

    def magic_loop(self, bm, edge, vert, connected, debug=False):
        # get "the face", that's not bordering the center edge
        edgefaces = [f for f in edge.link_faces]

        for loop in vert.link_loops:
            if loop.face not in edgefaces:
                face = loop.face

        # open bounds edge case
        if len(edgefaces) == 1:
            faceedges = edgefaces[0].edges
            for e in connected:
                if e not in faceedges:
                    if debug:
                        print("magic loop, open bounds")
                    return e

        # the 2 faces bordering the center edge
        f1 = edgefaces[0]
        f2 = edgefaces[1]

        # TODO: maybe you shouldnt get the face center medians and face normals, but instead the medians and normals of a triangle created form the face
        # should possibly deals better with non planar faces

        # face median centers
        m1co = f1.calc_center_median()  # NOTE: there's also calc_center_median_weighted()
        m2co = f2.calc_center_median()

        # move them both to the same distance from the edge, this ensures the resultuing loop is perfectly aligned with the edge
        if self.strict:
            # first get a center point on the edge
            medgeco = get_center_between_verts(vert, edge.other_vert(vert))

            # get the minium distance distances
            d1 = get_distance_between_points(medgeco, m1co)
            d2 = get_distance_between_points(medgeco, m2co)

            if d1 < d2:
                m2dir = m2co - medgeco
                m2co = medgeco + m2dir.normalized() * d1

            if d2 < d1:
                m1dir = m1co - medgeco
                m1co = medgeco + m1dir.normalized() * d2

        if debug:
            if self.strict:
                medge = bm.verts.new()
                medge.co = medgeco

            m1 = bm.verts.new()
            m1.co = m1co

            m2 = bm.verts.new()
            m2.co = m2co

        # points where face normals intersect "the face"
        i1co = mathutils.geometry.intersect_line_plane(m1co, m1co + f1.normal, vert.co, face.normal)
        i2co = mathutils.geometry.intersect_line_plane(m2co, m2co + f2.normal, vert.co, face.normal)

        if debug:
            i1 = bm.verts.new()
            i1.co = i1co

            i2 = bm.verts.new()
            i2.co = i2co

            i1edge = bm.edges.new((m1, i1))
            i2edge = bm.edges.new((m2, i2))

        # projecting the intersection points across the centeredge endpoint vert, "the vert"
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

        # point orthogonal to the crossedge in the direction of "the vert"( = the closest point on that vector to "the vert")
        crossvco, distance = mathutils.geometry.intersect_point_line(vert.co, crossv1co, crossv2co)

        # check the direction of the vert-crossv vector, against the other_vert-vert direction
        # if its not the same, the vert-crossv vector needs to be flipped, or rather the crossv vert needs to be on the other side
        vert_crossv = crossvco - vert.co
        othervert_vert = vert.co - edge.other_vert(vert).co

        dot = vert_crossv.dot(othervert_vert)

        if dot < 0:
            newdir = vert.co - crossvco
            crossvco = vert.co + newdir
            if debug:
                print("flipping the magic loop edge")

        crossv = bm.verts.new()
        crossv.co = crossvco

        loop = bm.edges.new((vert, crossv))

        if debug:
            print("magic loop")
        return loop

    def angle_loop(self, bm, vert, connected, debug=False):
        vert1 = connected[0].other_vert(vert)
        vert2 = connected[1].other_vert(vert)

        v = bm.verts.new()
        v.co = get_center_between_verts(vert1, vert2)

        e = bm.edges.new((vert, v))

        if debug:
            print("angle loop")
        return e

    def check_angle(self, edges):
        angle = get_angle_between_edges(edges[0], edges[1], radians=False)
        return angle

    def ngon_loop(self, ngon, edge, vert, debug=False):
        for e in ngon.edges:
            if e != edge and vert in e.verts:
                if debug:
                    print("ngon loop")
                return e

    def check_ngon(self, edge):
        for f in edge.link_faces:
            if len(f.verts) > 4:
                return f
        return False

    def simple_loop(self, seldict, edge, vert, debug=False):
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
            if debug:
                print("simple loop")
            return edges[0]
        else:  # take the edge with the biggest angle  to the center edge
            angle = 0
            for e in edges:
                a = get_angle_between_edges(edge, e, radians=False)
                if a > angle:
                    angle = a
                    loop = e
            if debug:
                print("simple loop, biggest angle")
            return loop

    def get_ring_edges(self, mesh):
        selfaceids = [f.index for f in mesh.polygons if f.select]
        seledgeids = [e.index for e in mesh.edges if e.select]

        m3.set_mode("EDIT")

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')
        bpy.ops.mesh.loop_multi_select(ring=True)
        m3.set_mode("OBJECT")

        ringedgeids = [e.index for e in mesh.edges if e.select and e.index in seledgeids]

        # select only the ring edges
        # for edge in mesh.edges:
            # if edge.index in ringedgeids:
                # edge.select = True
            # else:
                # edge.select = False

        # deselect all
        for edge in mesh.edges:
                edge.select = False

        return ringedgeids, selfaceids

    def debug_dict(self, seldict, showedges=False):
        for edge in seldict:
            print("edge:", edge)
            for vert in seldict[edge]:
                print(" » vert:", vert)
                if showedges:
                    for e in seldict[edge][vert]["connected"]:
                        print("   » edge:", e)
                print("   » loop:", seldict[edge][vert]["loop"])
                print("   » magic loop:", seldict[edge][vert]["magicloop"])
                print("   » handle:", seldict[edge][vert]["handle"])

        print()


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

        # bVerts = bm.verts
        bEdges = bm.edges
        # bFaces = bm.faces

        # verts = [v for v in bVerts if v.select]
        edges = [e for e in bEdges if e.select]
        # faces = [f for f in bFaces if f.select]

        # initialize dictionary
        seldict = {}
        for e in edges:
            seldict[e] = {}
            for vert in e.verts:
                seldict[e][vert] = {}
                seldict[e][vert]["connected"] = []
                seldict[e][vert]["loop"] = None
                for edge in vert.link_edges:
                    if edge != e and edge not in seldict[e][vert]["connected"]:
                        seldict[e][vert]["connected"].append(edge)

        # find/create loop edges
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
                        loop = self.magic_loop(bm, edge, vert, seldict[edge][vert]["connected"])
                        seldict[edge][vert]["loop"] = loop
                        loop.select = True

        self.debug_dict(seldict)

        bm.to_mesh(mesh)

        m3.set_mode("EDIT")

        return {'FINISHED'}

    def magic_loop(self, bm, edge, vert, connected, debug=False):
        # get the face, that's not bordering the center edge
        edgefaces = [f for f in edge.link_faces]

        for loop in vert.link_loops:
            if loop.face not in edgefaces:
                face = loop.face

        if len(edgefaces) == 1:
            faceedges = edgefaces[0].edges
            for e in connected:
                if e not in faceedges:
                    if debug:
                        print("magic loop, open bounds")
                    return e

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

        if debug:
            print("magic loop")
        return loop

    def angle_loop(self, bm, vert, connected, debug=False):
        vert1 = connected[0].other_vert(vert)
        vert2 = connected[1].other_vert(vert)

        v = bm.verts.new()
        v.co = vert1.co + (vert2.co - vert1.co) * 0.5

        e = bm.edges.new((vert, v))

        if debug:
            print("angle loop")
        return e

    def check_angle(self, edges):
        angle = get_angle_between_edges(edges[0], edges[1], radians=False)
        return angle

    def ngon_loop(self, ngon, edge, vert, debug=False):
        for e in ngon.edges:
            if e != edge and vert in e.verts:
                if debug:
                    print("ngon loop")
                return e

    def check_ngon(self, edge):
        for f in edge.link_faces:
            if len(f.verts) > 4:
                return f
        return False

    def simple_loop(self, seldict, edge, vert, debug=False):
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
            if debug:
                print("simple loop")
            return edges[0]
        else:  # take the edge with the biggest angle  to the center edge
            angle = 0
            for e in edges:
                a = get_angle_between_edges(edge, e, radians=False)
                if a > angle:
                    angle = a
                    loop = e
            if debug:
                print("simple loop, biggest angle")
            return loop

    def debug_dict(self, seldict, showedges=False):
        for edge in seldict:
            print("edge:", edge)
            for vert in seldict[edge]:
                print(" » vert:", vert)
                if showedges:
                    for e in seldict[edge][vert]["connected"]:
                        print("   » edge:", e)
                print("   » loop:", seldict[edge][vert]["loop"])

        print()


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

    tension = FloatProperty(name="Tension", default=1, min=0, max=2)

    cyclic = BoolProperty(name="Cyclic", default=False)
    capholes = BoolProperty(name="Cap Holes", default=False)
    captolerance = FloatProperty(name="Tolerance", default=0.01, min=0, max=0.2, precision=4, step=0.01)
    flip = BoolProperty(name="Flip", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "segments")
        column.prop(self, "tension")

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

        handles = create_handles(bVerts, rails, self.tension)

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


def create_handles(bVerts, rails, tension):
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

        # take the handles and and add in the tension
        handle1 = end1.co + ((h[0] - end1.co) * tension)
        handle2 = end2.co + ((h[1] - end2.co) * tension)

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


def get_center_between_verts(vert1, vert2):
    return vert1.co + (vert2.co - vert1.co) * 0.5


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


def get_distance_between_points(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def get_distance_between_verts(vert1, vert2, getvectorlength=True):
    if getvectorlength:
        vector = vert1.co - vert2.co
        return vector.length
    else:
        return math.sqrt((vert1.co[0] - vert2.co[0]) ** 2 + (vert1.co[1] - vert2.co[1]) ** 2 + (vert1.co[2] - vert2.co[2]) ** 2)
