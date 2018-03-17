import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty
import bmesh
from .. import M3utils as m3
import math
import mathutils


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
            hmm = bmesh.ops.bridge_loops(bm, edges=splineedges, use_cyclic=self.cyclic)
            print(hmm)

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


def get_distance(v1, v2):
    d = math.sqrt((v1.co[0] - v2.co[0]) ** 2 + (v1.co[1] - v2.co[1]) ** 2 + (v1.co[2] - v2.co[2]) ** 2)

    # you can also do the following:
    # direction = v1.co - v2.co
    # d2 = direction.length

    return d
