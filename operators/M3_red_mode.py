import bpy
from .. import M3utils as m3


# TODO: matcap selection


class RedMode(bpy.types.Operator):
    bl_idname = "machin3.red_mode"
    bl_label = "MACHIN3: Red Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        shadingmode = bpy.context.space_data.viewport_shade

        if shadingmode == "SOLID":
            self.switch_matcaps()
        elif shadingmode in ["MATERIAL", "RENDERED"]:
            self.change_bevel_color()

        return {'FINISHED'}

    def change_bevel_color(self):
        active = m3.get_active()

        if active:
            wstepmat = None
            for mat in active.data.materials:
                if mat.name.endswith("_wstep"):
                    wstepmat = mat

                    red = wstepmat.node_tree.nodes['RGB']

                    if red.mute is True:  # if it is muted, so tuened OFF
                        print("Turned red bevels ON.")
                        red.mute = False
                    else:
                        print("Turned red bevels OFF.")
                        red.mute = True
                    break

    def switch_matcaps(self):
        mc = bpy.context.space_data.matcap_icon
        if mc != '17':
            bpy.context.space_data.matcap_icon = '17'
        else:
            bpy.context.space_data.matcap_icon = '05'
