import bpy
from bpy.props import BoolProperty
from .. import M3utils as m3


class CenterCube(bpy.types.Operator):
    bl_idname = "machin3.center_cube"
    bl_label = "MACHIN3: Center Cube"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=True)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=False)

    autoeditmodescale = BoolProperty(name="Auto Edit Mode Scale", default=True)

    def execute(self, context):
        sel = m3.selected_objects()

        if len(sel) == 0:  # nothing object selected
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            active = m3.get_active()

            if self.axisx:
                active.location[0] = 0
            if self.axisy:
                active.location[1] = 0
            if self.axisz:
                active.location[2] = 0

            if self.autoeditmodescale:
                m3.set_mode("EDIT")
                m3.select_all("MESH")
                bpy.ops.transform.resize('INVOKE_DEFAULT', constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        else:  # objects selected
            for obj in sel:
                if self.axisx:
                    obj.location[0] = 0
                if self.axisy:
                    obj.location[1] = 0
                if self.axisz:
                    obj.location[2] = 0

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)
