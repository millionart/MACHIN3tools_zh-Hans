import bpy
from .. import M3utils as m3


class SmartModes(bpy.types.Operator):
    bl_idname = "machin3.smart_modes"
    bl_label = "MACHIN3: Smart Modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = m3.get_comp_mode()

        if mode == "VERT":
            try:
                bpy.ops.mesh.vert_connect_path()
            except:  # for it to fail by running it without a vert selection, or just a single vert
                bpy.ops.mesh.knife_tool('INVOKE_DEFAULT', use_occlude_geometry=True, only_selected=False)
        elif mode == "EDGE":
            bpy.ops.mesh.edge_rotate(use_ccw=False)
        elif mode == "FACE":
            bpy.ops.mesh.region_to_loop()

        return {'FINISHED'}
