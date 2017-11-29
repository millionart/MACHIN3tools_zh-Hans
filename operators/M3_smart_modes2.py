import bpy
from .. import M3utils as m3


class MoreSmartModes(bpy.types.Operator):
    bl_idname = "machin3.more_smart_modes"
    bl_label = "MACHIN3: More Smart Modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = m3.get_comp_mode()

        if mode in ["VERT", "EDGE"]:  # F2
            bpy.ops.mesh.f2('INVOKE_DEFAULT')
        elif mode == "FACE":
            facelist = m3.get_selection("FACE")
            if len(facelist) == 0:  # BISECT
                m3.select_all("MESH")
                bpy.ops.mesh.bisect('INVOKE_DEFAULT')
            else:  # DUPLICATE and SEPARATE
                bpy.ops.mesh.duplicate()
                bpy.ops.mesh.separate(type='SELECTED')
        return {'FINISHED'}
