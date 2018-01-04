import bpy
from bpy.props import FloatProperty, BoolProperty, IntProperty
from .. import M3utils as m3

# TODO: extend it to be cut from object mode where an intersecting cutter object determines the shape/polygon selection
# ####: or maybe make a second, simpler tool, might not need all the things Emboss has


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

    marksharp = BoolProperty(name="Mark Sharp", default=False)
    addbevelweight = BoolProperty(name="Add Bevel Weight", default=False)
    bevelweight = FloatProperty(name="Weight", default=1, min=0, max=1)

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        column.prop(self, "outerinset")
        column.prop(self, "innerinset")
        column.prop(self, "depth")
        column.prop(self, "invert")

        column.separator()

        row = column.row()
        row.prop(self, "individual")
        row.prop(self, "individualgap")

        row = column.split(percentage=0.2)
        row.prop(self, "bevel")
        row.prop(self, "bevelamount")
        row.prop(self, "bevelsegments")

        column.separator()

        column.prop(self, "marksharp")
        row = column.row()
        row.prop(self, "addbevelweight")
        row.prop(self, "bevelweight")

    def execute(self, context):
        self.scene_scale = m3.get_scene_scale()
        self.outer = self.outerinset / 100 / self.scene_scale
        self.gap = self.individualgap / 100 / self.scene_scale
        self.inner = self.innerinset / 100 / self.scene_scale
        self.d = - self.depth / 4 / self.scene_scale
        self.amount = self.bevelamount / 100 / self.scene_scale
        self.bweight = self.bevelweight

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

        # clear any existing bevel weights and sharps
        bpy.ops.transform.edge_bevelweight(value=-1)
        bpy.ops.mesh.mark_sharp(clear=True)

        # create temporary base and inset materials and bottom materials, used to select specific polygons
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

        mat = bpy.data.materials.get("temp_bottom")

        if mat:
            tempbottommat = mat
        else:
            tempbottommat = bpy.data.materials.new("temp_bottom")
            tempbottommat.diffuse_color = (0.1, 1, 0.1)

        # append them
        if tempbasemat.name not in active.data.materials:
            active.data.materials.append(tempbasemat)
        if tempinsetmat.name not in active.data.materials:
            active.data.materials.append(tempinsetmat)
        if tempbottommat.name not in active.data.materials:
            active.data.materials.append(tempbottommat)

        # find the slots of the temp mats
        for idx, slot in enumerate(active.material_slots):
            if slot.material.name == "temp_base":
                tempbaseslot = idx
                tempinsetslot = idx + 1
                tempbottomslot = idx + 2
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

        if len(faces) > 1:  # with just 1 polygon selected individual doesnt work, as there are no interior edges
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

        # assign the bottom mat
        active.active_material_index = tempbottomslot
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

            m3.unselect_all("MESH")
            m3.set_mode("FACE")

        if self.marksharp or self.addbevelweight:
            # select the "bottom" polygons
            m3.set_mode("OBJECT")

            # shade smooth while in object mode
            bpy.ops.object.shade_smooth()

            # also enable auto-smooth
            active.data.use_auto_smooth = True

            # to selct the "wall" polygons, first select the bottom polys
            mesh = bpy.context.active_object.data

            for f in mesh.polygons:
                if f.material_index == tempbottomslot:
                    f.select = True
                else:
                    f.select = False
            m3.set_mode("EDIT")

            # increase selection
            bpy.ops.mesh.select_more()

            # deselect the bottom polygons
            m3.set_mode("OBJECT")

            for f in mesh.polygons:
                if f.material_index == tempbottomslot:
                    f.select = False
            m3.set_mode("EDIT")

            # boundary loop
            bpy.ops.mesh.region_to_loop()

            # mark sharp
            if self.marksharp:
                bpy.ops.mesh.mark_sharp()

            # add bevelweight
            if self.addbevelweight:
                bpy.ops.transform.edge_bevelweight(value=self.bweight)

        # remove the temp materials again
        m3.set_mode("OBJECT")
        active.active_material_index = tempinsetslot
        bpy.ops.object.material_slot_remove()
        active.active_material_index = tempbaseslot
        bpy.ops.object.material_slot_remove()
        active.active_material_index = tempbottomslot
        bpy.ops.object.material_slot_remove()
        m3.set_mode("EDIT")
        m3.set_mode("FACE")

        # remove potential double verts
        if self.outerinset == 0:
            print("Removing duplicate verts at the outer insert.")
            bpy.ops.mesh.select_more()
            bpy.ops.mesh.select_more()
            bpy.ops.mesh.remove_doubles()

        m3.unselect_all("MESH")
