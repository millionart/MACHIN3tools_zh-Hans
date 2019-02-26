import bpy


class CursorToOrigin(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_origin"
    bl_label = "MACHIN3: Cursor to Origin"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.cursor_location.zero()
        context.scene.cursor_rotation_mode = 'XYZ'
        context.scene.cursor_rotation_euler.zero()

        return {'FINISHED'}
