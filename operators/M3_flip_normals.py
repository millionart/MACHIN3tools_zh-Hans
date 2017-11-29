import bpy
from .. import M3utils as m3


class FlipNormals(bpy.types.Operator):
    bl_idname = "machin3.flip_normals"
    bl_label = "MACHIN3: Flip Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in m3.selected_objects():
            print("Flipping '%s." % (obj.name))
            m3.make_active(obj)

            m3.set_mode("EDIT")
            m3.unhide_all("MESH")
            m3.select_all("MESH")

            bpy.ops.mesh.flip_normals()

            m3.unselect_all("MESH")
            m3.set_mode("OBJECT")
        return {'FINISHED'}
