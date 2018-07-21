import bpy
from bpy.props import EnumProperty
from ... utils import MACHIN3 as m3


axisitems = [("FRONT", "Front", ""),
             ("BACK", "Back", ""),
             ("LEFT", "Left", ""),
             ("RIGHT", "Right", ""),
             ("TOP", "Top", ""),
             ("BOTTOM", "Bottom", "")]


class ViewAxis(bpy.types.Operator):
    bl_idname = "machin3.view_axis"
    bl_label = "View Axis"
    bl_description = "Click: Align View\nALT + Click: Align View to Active"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(name="Axis", items=axisitems, default="FRONT")


    def invoke(self, context, event):

        if event.alt:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=True)
        else:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=False)

        return {'FINISHED'}
