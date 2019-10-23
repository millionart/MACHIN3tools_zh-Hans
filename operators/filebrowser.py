import bpy
from bpy.props import StringProperty
from .. utils.system import abspath, open_folder


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
