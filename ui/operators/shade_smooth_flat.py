import bpy
from ... utils import MACHIN3 as m3



class ShadeSmooth(bpy.types.Operator):
    bl_idname = "machin3.shade_smooth"
    bl_label = "Shade Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.mode == "OBJECT":
            bpy.ops.object.shade_smooth()
        elif context.mode == "EDIT_MESH":
            bpy.ops.mesh.faces_shade_smooth()

        return {'FINISHED'}


class ShadeFlat(bpy.types.Operator):
    bl_idname = "machin3.shade_flat"
    bl_label = "Shade Flat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.mode == "OBJECT":
            bpy.ops.object.shade_flat()
        elif context.mode == "EDIT_MESH":
            bpy.ops.mesh.faces_shade_flat()

        return {'FINISHED'}
