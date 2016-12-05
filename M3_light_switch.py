bl_info = {
    "name": "Light Switch",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu, Mouse Button 5",
    "description": "Switch Theme and Matcap at the same time",
    "warning": "",
    "wiki_url": "",
    "category": "Interface"}

# SETTINGS

themelocation = "/home/%USERNAME/.config/blender/2.77/scripts/presets/interface_theme/"  # change appropriately
lighttheme = "flatcream.xml"  # http://www.blendswap.com/blends/view/77937
darktheme = "rtheme.xml"
lightmatcap = "01"
darkmatcap = "05"

button = "BUTTON5MOUSE"
press = "PRESS"
ctrl = True
alt = False
shift = False
state = 0   # default/start-up theme (dark)

import bpy
import os


class LightSwitch(bpy.types.Operator):
    bl_idname = "machin3.light_switch"
    bl_label = "MACHIN3: Light Switch"

    def execute(self, context):
        global state
        if state == 0:
            print("switching the light on!")
            bpy.ops.script.execute_preset(filepath=os.path.join(themelocation, lighttheme), menu_idname="USERPREF_MT_interface_theme_presets")
            bpy.context.space_data.matcap_icon = lightmatcap
            state = 1
        else:
            print("switching the light off!")
            bpy.ops.script.execute_preset(filepath=os.path.join(themelocation, darktheme), menu_idname="USERPREF_MT_interface_theme_presets")
            bpy.context.space_data.matcap_icon = darkmatcap
            state = 0
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LightSwitch)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new(LightSwitch.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(LightSwitch)


if __name__ == "__main__":
    register()
