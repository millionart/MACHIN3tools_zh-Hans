import bpy
from .. utils import MACHIN3 as m3



class SmartEdge(bpy.types.Operator):
    bl_idname = "machin3.smart_edge"
    bl_label = "MACHIN3: Smart Edge"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return m3.get_mode() in ["VERT", "EDGE", "FACE"]

    def execute(self, context):
        mode = m3.get_mode()

        if mode == "VERT":
            selverts = m3.get_selection("VERT")

            # KNIFE

            if len(selverts) < 2:
                bpy.ops.mesh.knife_tool('INVOKE_DEFAULT')

            # PATH CONNECT

            else:
                try:
                    bpy.ops.mesh.vert_connect_path()

                except:  # invalid selection order
                    pass

        elif mode == "EDGE":
            seledges = m3.get_selection("EDGE")

            # TURN EDGE

            if 1 <= len(seledges) < 4:
                bpy.ops.mesh.edge_rotate(use_ccw=False)

            # LOOP TO REGION

            if len(seledges) >= 4:
                bpy.ops.mesh.loop_to_region()
                m3.set_mode("FACE")

        # REGION TO LOOP

        elif mode == "FACE":
            # NOTE, there seems to be an issue, where blender doesn't update the mode properly
            # futhermore, I can't manually update if after region to loop either
            # doing it before works however
            m3.set_mode("EDGE")

            bpy.ops.mesh.region_to_loop()

        return {'FINISHED'}
