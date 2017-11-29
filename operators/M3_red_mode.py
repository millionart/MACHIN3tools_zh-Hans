import bpy
from bpy.props import StringProperty
from .. import M3utils as m3


class RedMode(bpy.types.Operator):
    bl_idname = "machin3.red_mode"
    bl_label = "MACHIN3: Red Mode"
    bl_options = {'REGISTER', 'UNDO'}

    defaultmatcap = StringProperty(name="Default Matcap", default="05")
    redmatcap = StringProperty(name="Red Matcap", default="17")

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        mc = bpy.context.space_data.matcap_icon

        if mc != self.defaultmatcap:
            view = context.space_data
            column.template_icon_view(view, "matcap_icon")

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
            if active.type == "MESH":
                wstepmat = None
                for mat in active.data.materials:
                    if mat is not None:
                        if mat.name.endswith("_wstep"):
                            wstepmat = mat

                            red = wstepmat.node_tree.nodes['RGB']

                            if red.mute is True:  # it is muted, so the red bevels are turned OFF
                                print("Turned red bevels ON.")
                                red.mute = False
                            else:
                                print("Turned red bevels OFF.")
                                red.mute = True
                            break

    def switch_matcaps(self):
        mc = bpy.context.space_data.matcap_icon

        if mc == self.redmatcap:
            bpy.context.space_data.matcap_icon = self.defaultmatcap
        else:
            if mc == self.defaultmatcap:
                bpy.context.space_data.matcap_icon = self.redmatcap
            else:
                self.redmatcap = mc
                bpy.context.space_data.matcap_icon = self.redmatcap
