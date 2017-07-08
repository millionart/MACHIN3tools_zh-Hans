import bpy
from bpy.props import BoolProperty
from .. import M3utils as m3


class MirrorX(bpy.types.Operator):
    bl_idname = "machin3.mirror_x"
    bl_label = "MACHIN3: Mirror X"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=True)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=False)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    DMcustomNormals = BoolProperty(name="re-do custom Normals", default=True)
    DMcopiedNormals = BoolProperty(name="move copied Normals to end of stack", default=True)

    def execute(self, context):
        mirror(self)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

        if m3.DM_check():
            column.separator()

            column.label("DECALmachine - UVs")
            row = column.row(align=True)
            row.prop(self, "DMmirrorU", toggle=True)
            row.prop(self, "DMmirrorV", toggle=True)

            column.separator()

            column.label("DECALmachine - custom Normals")
            column.prop(self, "DMcustomNormals")
            column.prop(self, "DMcopiedNormals")


class MirrorY(bpy.types.Operator):
    bl_idname = "machin3.mirror_y"
    bl_label = "MACHIN3: Mirror Y"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=True)
    axisz = BoolProperty(name="Z", default=False)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    def execute(self, context):
        mirror(self.axisx, self.axisy, self.axisz)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

        if m3.DM_check():
            column.separator()

            column.label("DECALmachine - UVs")
            row = column.row(align=True)
            row.prop(self, "DMmirrorU", toggle=True)
            row.prop(self, "DMmirrorV", toggle=True)

            column.separator()

            column.label("DECALmachine - custom Normals")
            column.prop(self, "DMcustomNormals")
            column.prop(self, "DMcopiedNormals")


class MirrorZ(bpy.types.Operator):
    bl_idname = "machin3.mirror_z"
    bl_label = "MACHIN3: Mirror Z"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=True)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    def execute(self, context):
        mirror(self.axisx, self.axisy, self.axisz)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

        if m3.DM_check():
            column.separator()

            column.label("DECALmachine - UVs")
            row = column.row(align=True)
            row.prop(self, "DMmirrorU", toggle=True)
            row.prop(self, "DMmirrorV", toggle=True)

            column.separator()

            column.label("DECALmachine - custom Normals")
            column.prop(self, "DMcustomNormals")
            column.prop(self, "DMcopiedNormals")


def mirror(self):
    active = m3.get_active()
    selection = m3.selected_objects()

    if len(selection) > 1:
        selection.remove(active)

        for obj in selection:
            if obj.type == "MESH":
                m3.unselect_all("OBJECT")
                obj.select = True

                mirror = obj.modifiers.new(name="M3_mirror", type="MIRROR")

                mirror.use_x = self.axisx
                mirror.use_y = self.axisy
                mirror.use_z = self.axisz

                mirror.mirror_object = active

                if m3.DM_check():
                    # DECALmachine support (u or v mirror for parallax and for info decals!)
                    if "decal" in obj.name or "info" in obj.name:
                        if self.DMmirrorU:
                            mirror.use_mirror_u = True
                        if self.DMmirrorV:
                            mirror.use_mirror_v = True

                    # DECALmachine wstep.create_weighted_normals() support
                    if self.DMcustomNormals:
                        mod = obj.modifiers.get("M3_custom_normals")
                        if mod:
                            showinviewport = mod.show_viewport

                            active.select = False
                            bpy.ops.machin3.wstep()  # needs to wstep, because we need to get the mirror also on the target, re-stepping seems be the easiest way to do it
                            active.select = True

                            # take the show_viewport parameter from the previous data_transfer (needs to be done through extra variable for some reason
                            newmod = obj.modifiers.get("M3_custom_normals")
                            newmod.show_viewport = showinviewport

                    # DECALmachine wstep.copy_normals() support
                    if self.DMcopiedNormals:
                        mod = obj.modifiers.get("M3_copied_normals")
                        if mod:
                            # making obj active for ops
                            m3.make_active(obj)
                            while obj.modifiers[-1].name != "M3_copied_normals":
                                bpy.ops.object.modifier_move_down(modifier="M3_copied_normals")
                            # setting the original active back again
                            m3.make_active(active)

        for obj in selection:
            obj.select = True

        active.select = True
    else:
        print("Mirror: Select at least 2 objects.")
