import bpy
from bpy.props import FloatProperty, BoolProperty, IntProperty
from .. import M3utils as m3


class Emboss(bpy.types.Operator):
    bl_idname = "machin3.emboss"
    bl_label = "MACHIN3: Emboss"
    bl_options = {'REGISTER', 'UNDO'}

    outerinset = FloatProperty(name="Outer Inset", default=20, min=0)
    innerinset = FloatProperty(name="Inner Inset", default=20, min=0)

    individual = BoolProperty(name="Individual", default=False)
    individualgap = FloatProperty(name="Gap", default=10, min=0.01)

    bevel = BoolProperty(name="Bevel", default=False)
    bevelamount = FloatProperty(name="Amount", default=5, min=0.01)
    bevelsegments = IntProperty(name="Segments", default=1, min=1)

    depth = FloatProperty(name="Depth", default=1, min=0)
    invert = BoolProperty(name="Invert", default=False)

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        column.prop(self, "outerinset")
        column.prop(self, "innerinset")

        row = column.row()
        row.prop(self, "individual")
        row.prop(self, "individualgap")

        row = column.split(percentage=0.2)
        row.prop(self, "bevel")
        row.prop(self, "bevelamount")
        row.prop(self, "bevelsegments")

        column.prop(self, "depth")
        column.prop(self, "invert")

    def execute(self, context):
        self.scene_scale = m3.get_scene_scale()
        self.outer = self.outerinset / 100 / self.scene_scale
        self.gap = self.individualgap / 100 / self.scene_scale
        self.inner = self.innerinset / 100 / self.scene_scale
        self.d = - self.depth / 4 / self.scene_scale
        self.amount = self.bevelamount / 100 / self.scene_scale
        if self.invert:
            self.d = abs(self.d)

        active = m3.get_active()

        # get currently selected faces
        faces = m3.get_selection("FACE")

        if len(faces) > 0:
            self.emboss(active, faces)
        else:
            self.report({'ERROR'}, "Select at least one polygon!")

        return {'FINISHED'}

    def emboss(self, active, faces):
        # outer inset
        bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, thickness=self.outer, depth=0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=True)

        # get currently selected faces
        faces = m3.get_selection("FACE")

        # create temporary base and inset materials
        mat = bpy.data.materials.get("temp_base")

        if mat:
            tempbasemat = mat
        else:
            tempbasemat = bpy.data.materials.new("temp_base")
            tempbasemat.diffuse_color = (0.1, 0.1, 0.1)

        mat = bpy.data.materials.get("temp_inset")

        if mat:
            tempinsetmat = mat
        else:
            tempinsetmat = bpy.data.materials.new("temp_inset")
            tempinsetmat.diffuse_color = (1, 0.1, 0.1)

        # append both
        if tempbasemat.name not in active.data.materials:
            active.data.materials.append(tempbasemat)
        if tempinsetmat.name not in active.data.materials:
            active.data.materials.append(tempinsetmat)

        # find the slots of the temp mats
        for idx, slot in enumerate(active.material_slots):
            if slot.material.name == "temp_base":
                tempbaseslot = idx
                tempinsetslot = idx + 1
                break

        # assign the tempbase material to everything
        m3.select_all("MESH")
        active.active_material_index = tempbaseslot
        bpy.ops.object.material_slot_assign()

        # select and assign the tempinsetmat to the initial face selection
        m3.unselect_all("MESH")
        m3.make_selection("FACE", faces)
        active.active_material_index = tempinsetslot
        bpy.ops.object.material_slot_assign()

        if self.individual:
            # select the gap edges
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')

            bpy.ops.mesh.bevel(offset=self.gap, vertex_only=False)

            m3.set_mode("FACE")

            active.active_material_index = tempbaseslot
            bpy.ops.object.material_slot_assign()

            # select the inner inset polygons
            m3.set_mode("OBJECT")
            mesh = bpy.context.active_object.data

            for f in mesh.polygons:
                if f.material_index == tempinsetslot:
                    f.select = True
                else:
                    f.select = False
            m3.set_mode("EDIT")

        # inner inset
        bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, thickness=self.inner, depth=self.d, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=True)

        # remove the insetmaterial from the "bottom" polys
        active.active_material_index = tempbaseslot
        bpy.ops.object.material_slot_assign()

        if self.bevel:
            # select the "wall" polygons
            m3.set_mode("OBJECT")
            mesh = bpy.context.active_object.data

            for f in mesh.polygons:
                if f.material_index == tempinsetslot:
                    f.select = True
                else:
                    f.select = False
            m3.set_mode("EDIT")

            # select the corner edges
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')

            # bevel the corners
            bpy.ops.mesh.bevel(offset=self.amount, segments=self.bevelsegments, vertex_only=False)

        # remove the temp materials again
        m3.set_mode("OBJECT")
        active.active_material_index = tempinsetslot
        bpy.ops.object.material_slot_remove()
        active.active_material_index = tempbaseslot
        bpy.ops.object.material_slot_remove()
        m3.set_mode("EDIT")
        m3.set_mode("FACE")
