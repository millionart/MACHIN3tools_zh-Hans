bl_info = {
    "name": "Focus",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu/ CTRL + F",
    "description": "Disables all Mirror modifiers of the selected objects, then enters local view. Renables mirror modifers again, when exiting localview.",
    "warning": "",
    "wiki_url": "",
    "category": "Interface"}

# SETTINGS

button = "F"
press = "PRESS"
ctrl = True
alt = False
shift = False

import bpy


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"

    def execute(self, context):
        localview = self.get_localview()
        if not localview:  # entering focus mode(local view)
            self.mirror("HIDE")
            bpy.ops.view3d.localview()
        else:  # leaving focus mode(local view)
            self.mirror("SHOW")
            bpy.ops.view3d.localview()
        return {'FINISHED'}

    def mirror(self, string):
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj

            activeobj = bpy.context.scene.objects.active

            mods = list(activeobj.modifiers)
            for mod in mods:
                if "Mirror" in mod.name or "mirror_mirror" in mod.name:
                    print("found mirror: %s" % (mod.name))
                    if string == "HIDE":
                        mod.show_viewport = False
                    elif string == "SHOW":
                        mod.show_viewport = True

    def get_localview(self):
        localview = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                if area.spaces.active.local_view is not None:
                    localview = True
        return localview


def register():
    bpy.utils.register_class(Focus)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new(Focus.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(Focus)

    # TODO: properly unregisgter keymap and keymap_items


if __name__ == "__main__":
    register()
