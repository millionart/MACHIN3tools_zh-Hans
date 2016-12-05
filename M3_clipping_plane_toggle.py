bl_info = {
    "name": "Clipping Plane Toggle",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu, Mouse Button 5",
    "description": "Toggle through different clipping plane settings",
    "warning": "",
    "wiki_url": "",
    "category": "Interface"}

# SETTINGS

button = "BUTTON5MOUSE"
press = "PRESS"
ctrl = False
alt = False
shift = False
state = 0  # aka 0.1, default/start-up scene setting

import bpy


class ClippingToggle(bpy.types.Operator):
    bl_idname = "machin3.clipping_plane_toggle"
    bl_label = "MACHIN3: Clipping Plane Toggle"

    def execute(self, context):
        global state

        if state == 0:
            bpy.context.space_data.clip_start = 0.01
            state += 1
        elif state == 1:
            bpy.context.space_data.clip_start = 0.001
            state += 1
        elif state == 2:
            bpy.context.space_data.clip_start = 0.1
            state = 0
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ClippingToggle)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new(ClippingToggle.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(ClippingToggle)


if __name__ == "__main__":
    register()
