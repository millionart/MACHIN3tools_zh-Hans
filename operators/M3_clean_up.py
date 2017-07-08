import bpy

from bpy.props import BoolProperty, EnumProperty, FloatProperty
from .. import M3utils as m3


# TODO: check out 534_003a.blend and figure out why remove 2 edged isnt working

selectchoice = [("NONE", "None", ""),
                ("MANIFOLD", "Manifold", ""),
                ("TRIS", "Tris", ""),
                ("NGONS", "Ngons", "")]


class CleansUpGood(bpy.types.Operator):
    bl_idname = "machin3.clean_up"
    bl_label = "MACHIN3: Cleans Up Good"
    bl_options = {'REGISTER', 'UNDO'}

    removedoubles = BoolProperty(name="Remove Doubles", default=True)
    removethreshold = FloatProperty(name="Threshold", default=1)
    removedegenerates = BoolProperty(name="Remove Degenerates (also removes doubles!)", default=True)
    remove2edged = BoolProperty(name="Remove 2-Edged Verts (experimental)", default=True)
    deleteloose = BoolProperty(name="Delete Loose", default=True)
    deletelooseincludefaces = BoolProperty(name=" incl. Faces", default=False)
    recalcnormals = BoolProperty(name="Recalculate Normals", default=True)

    select = EnumProperty(name="Select", items=selectchoice, default="MANIFOLD")

    view_selected = BoolProperty(name="View Selected", default=False)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        row.prop(self, "removedoubles")
        row.prop(self, "removethreshold")

        col.prop(self, "removedegenerates")
        col.prop(self, "remove2edged")

        row = col.split()
        row.prop(self, "deleteloose")
        row.prop(self, "deletelooseincludefaces")

        col.prop(self, "recalcnormals")

        col.label("Select")
        row = col.row()
        row.prop(self, "select", expand=True)

        col.prop(self, "view_selected", toggle=True)

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
        else:
            print("Unsupported component mode.")

        return {'FINISHED'}

    def clean_up(self, mode):  # needs to be in edit mode
        m3.select_all("MESH")

        if self.removedoubles:
            bpy.ops.mesh.remove_doubles(threshold=self.removethreshold / 10000)

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

        if self.select == "NONE":
            if self.remove_2_edged_verts:  # leaves you in vert mode
                if mode == "EDGE":
                    m3.set_mode("EDGE")
                elif mode == "FACE":
                    m3.set_mode("FACE")
        elif self.select == "MANIFOLD":
            # select non-manifold geometry, helpful to find holes
            # also helpful for finding overlapping bevels too and rarely invisible/undetectable vertices, both of which can prevent booleans to work
            if mode in["VERT", "EDGE"]:
                bpy.ops.mesh.select_non_manifold()  # will work in either vert or edge mode, but not in face mode
                if mode == "EDGE":
                    m3.set_mode("EDGE")
            else:
                m3.set_mode("VERT")
                bpy.ops.mesh.select_non_manifold()
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='FACE')  # manifold selection(loop of verts or edges) is by default not converted to faces, unless a face it encircled, hence use_expand
        elif self.select in ["TRIS", "NGONS"]:
            if self.select == "TRIS":
                bpy.ops.mesh.select_face_by_sides(number=3)
            else:
                bpy.ops.mesh.select_face_by_sides(number=4, type="GREATER")
            if self.remove_2_edged_verts:  # leaves you in vert mode
                if mode == "EDGE":
                    m3.set_mode("EDGE")
                elif mode == "FACE":
                    m3.set_mode("FACE")

        if self.view_selected:
            bpy.ops.view3d.view_selected(use_all_regions=False)

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
