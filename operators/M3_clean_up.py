import bpy

from bpy.props import BoolProperty
from .. import M3utils as m3


# TODO: select tris and ngons!


class CleansUpGood(bpy.types.Operator):
    bl_idname = "machin3.clean_up"
    bl_label = "MACHIN3: Cleans Up Good"
    bl_options = {'REGISTER', 'UNDO'}

    removedoubles = BoolProperty(name="Remove Doubles", default=True)
    removedegenerates = BoolProperty(name="Remove Degenerates (also removes doubles!)", default=True)
    remove2edged = BoolProperty(name="Remove 2-Edged Verts", default=True)
    deleteloose = BoolProperty(name="Delete Loose", default=True)
    deletelooseincludefaces = BoolProperty(name=" incl. Faces", default=False)
    recalcnormals = BoolProperty(name="Recalculate Normals", default=True)
    selectnonmanifold = BoolProperty(name="Select Non-Manifold", default=True)

    def execute(self, context):
        mode = m3.get_mode()

        if mode == "OBJECT":
            for obj in bpy.context.selected_objects:
                if obj.type == "MESH":
                    print(obj.name)
                    m3.make_active(obj)
                    m3.set_mode("EDIT")
                    m3.set_mode("VERT")
                    self.clean_up("VERT")
                    m3.set_mode("OBJECT")
        elif mode in ["VERT", "EDGE", "FACE"]:
            self.clean_up(mode)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "removedoubles")
        col.prop(self, "removedegenerates")
        col.prop(self, "remove2edged")

        row = col.split()
        row.prop(self, "deleteloose")
        row.prop(self, "deletelooseincludefaces")

        col.prop(self, "recalcnormals")
        col.prop(self, "selectnonmanifold")

    def clean_up(self, mode):  # needs to be in edit mode
        m3.select_all("MESH")

        if self.removedoubles:
            bpy.ops.mesh.remove_doubles()

        # dissolve degenerates
        if self.removedegenerates:
            bpy.ops.mesh.dissolve_degenerate()

        # recalculate normals
        if self.recalcnormals:
            bpy.ops.mesh.normals_make_consistent(inside=False)

        # delete loose geometry (except faces)
        if self.deleteloose:
            if self.deletelooseincludefaces:
                bpy.ops.mesh.delete_loose(use_faces=True)
            else:
                bpy.ops.mesh.delete_loose(use_faces=False)

        m3.unselect_all("MESH")

        # dissolve two-edged vertices, will go into vertex mode
        if self.remove2edged:
            self.remove_2_edged_verts()

        # select non-manifold geometry, helpful to find holes
        # also helpful for finding overlapping bevels too and rarely invisible/undetectable vertices, both of which can prevent booleans to work
        if self.selectnonmanifold:
            if mode in["VERT", "EDGE"]:
                bpy.ops.mesh.select_non_manifold()  # will work in either vert or edge mode, but not in face mode
                if mode == "EDGE":
                    m3.set_mode("EDGE")
            else:
                m3.set_mode("VERT")
                bpy.ops.mesh.select_non_manifold()
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='FACE')

    def remove_2_edged_verts(self):
        mesh = bpy.context.object.data

        # get vertex count
        m3.set_mode("OBJECT")
        count = len(mesh.vertices)

        # select first edge
        mesh.edges[0].select = True
        m3.set_mode("EDIT")

        # create 2-edged vert
        bpy.ops.mesh.subdivide(smoothness=0)
        m3.unselect_all("MESH")

        # select newest vert
        m3.set_mode("OBJECT")
        mesh.vertices[-1].select = True
        m3.set_mode("EDIT")

        # select similar
        m3.set_mode("VERT")
        bpy.ops.mesh.select_similar(type='EDGE', threshold=0.01)

        # limited dissolve
        bpy.ops.mesh.dissolve_limited()
        m3.unselect_all("MESH")

        # fetch new vertex count
        m3.set_mode("OBJECT")
        newcount = len(mesh.vertices)
        m3.set_mode("EDIT")

        print("Info: Removed: %d two-edged vertices" % (count - newcount))
