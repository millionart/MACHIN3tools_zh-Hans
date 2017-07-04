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

    def execute(self, context):
        mirror(self.axisx, self.axisy, self.axisz)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)


class MirrorY(bpy.types.Operator):
    bl_idname = "machin3.mirror_y"
    bl_label = "MACHIN3: Mirror Y"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=True)
    axisz = BoolProperty(name="Z", default=False)

    def execute(self, context):
        mirror(self.axisx, self.axisy, self.axisz)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)


class MirrorZ(bpy.types.Operator):
    bl_idname = "machin3.mirror_z"
    bl_label = "MACHIN3: Mirror Z"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=True)

    def execute(self, context):
        mirror(self.axisx, self.axisy, self.axisz)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)


def mirror(axisx, axisy, axisz):
    active = m3.get_active()
    selection = m3.selected_objects()
    selection.remove(active)

    for obj in selection:
        mirror = obj.modifiers.new(name="M3_mirror", type="MIRROR")

        mirror.use_x = axisx
        mirror.use_y = axisy
        mirror.use_z = axisz

        mirror.mirror_object = active

        # DECALmachine support (u mirror for parallax and for info decals!)
        if "decal" in obj.name or "info" in obj.name:
            mirror.use_mirror_u = True

        # DECALmachine wstep.create_weighted_normals() support
        mod = obj.modifiers.get("M3_custom_normals")
        if mod:
            active.select = False
            bpy.ops.machin3.wstep()  # needs to wstep, because we need to get the mirror also on the target, re-stepping seems be the easiest way to do it
            active.select = True

        # DECALmachine wstep.copy_normals() support
        mod = obj.modifiers.get("M3_copied_normals")
        if mod:
            # making obj active for ops
            m3.make_active(obj)
            while obj.modifiers[-1].name != "M3_copied_normals":
                bpy.ops.object.modifier_move_down(modifier="M3_copied_normals")
            # setting the original active back again
            m3.make_active(active)
