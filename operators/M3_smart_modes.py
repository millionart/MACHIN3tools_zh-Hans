import bpy
from .. import M3utils as m3


class SmartModes(bpy.types.Operator):
    bl_idname = "machin3.smart_modes"
    bl_label = "MACHIN3: Smart Modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = m3.get_comp_mode()

        if mode == "VERT":
            vertlist = m3.get_selection("VERT")
            if len(vertlist) < 2:
                bpy.ops.mesh.knife_tool('INVOKE_DEFAULT')
            else:
                try:
                    bpy.ops.mesh.vert_connect_path()
                except:  # invalid selection order
                    pass
        elif mode == "EDGE":
            edgelist = m3.get_selection("EDGE")
            if len(edgelist) == 0:
                pass
            elif len(edgelist) < 3:  # you need at least 3 edges to mark a boundary, so anything below can be used for turning instead
                bpy.ops.mesh.edge_rotate(use_ccw=False)
            else:
                bpy.ops.mesh.region_to_loop()
        elif mode == "FACE":
            bpy.ops.mesh.region_to_loop()

        return {'FINISHED'}
