import bpy
from bpy.props import StringProperty
import os


class FilebrowserDelete(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_delete"
    bl_label = "Delete File from Disk"
    bl_description = "Delete Files in the Filebrowser"
    bl_options = {'REGISTER', 'UNDO'}

    path: StringProperty(name="Path")

    def invoke(self, context, event):
        wm = context.window_manager
        area = context.area

        if area.type == 'FILE_BROWSER':
            params = area.spaces[0].params

            directory = params.directory
            filename = params.filename

            if directory and filename:
                path = os.path.join(directory, filename)

                if path and os.path.exists(path):
                    self.path = path

                    return wm.invoke_confirm(self, event)
        return {'FINISHED'}

    def execute(self, context):
        os.unlink(self.path)
        print("Deleted", self.path)

        bpy.ops.file.refresh()
        return {'FINISHED'}
