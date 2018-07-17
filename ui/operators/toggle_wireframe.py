import bpy
from ... utils import MACHIN3 as m3



class ToggleWireframe(bpy.types.Operator):
    bl_idname = "machin3.toggle_wireframe"
    bl_label = "Toggle Wireframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        overlay = context.space_data.overlay
        shading = context.space_data.shading

        if context.mode == "OBJECT":
            overlay.show_wireframes = not overlay.show_wireframes
        elif context.mode == "EDIT_MESH":
            shading.show_xray = not shading.show_xray

        return {'FINISHED'}
