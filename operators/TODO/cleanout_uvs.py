import bpy
from .. import M3utils as m3


class CleanoutUVs(bpy.types.Operator):
    bl_idname = "machin3.cleanout_uvs"
    bl_label = "MACHIN3: Cleanout UVs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = m3.selected_objects()

        for obj in selection:
            if obj.type == "MESH":
                m3.make_active(obj)

                uvs = obj.data.uv_textures

                while uvs:
                    print(" > removing UVs: %s" % (uvs[0].name))
                    uvs.remove(uvs[0])

        return {'FINISHED'}
