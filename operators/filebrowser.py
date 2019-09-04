import bpy
from bpy.props import StringProperty
import os
from .. utils.system import abspath, open_folder


class Delete(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_delete"
    bl_label = "Delete File from Disk"
    bl_description = "Delete Files in the Filebrowser"
    bl_options = {'REGISTER', 'UNDO'}

    path: StringProperty(name="Path")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER'

    def invoke(self, context, event):
        wm = context.window_manager

        params = context.space_data.params

        directory = params.directory.decode()
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


class Open(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_open"
    bl_label = "MACHIN3: Open in System's filebrowser"
    bl_description = "Open the current location in the System's own filebrowser"
    bl_options = {'REGISTER', 'UNDO'}

    path: StringProperty(name="Path")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER'

    def execute(self, context):
        params = context.space_data.params

        directory = abspath(params.directory.decode())

        open_folder(directory)

        return {'FINISHED'}
