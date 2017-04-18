bl_info = {
    "name": "Multi Mirror Mirror",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu/ Shift + Alt + X/Y/Z",
    "description": "Mirror Mirror Tool, but allows mirroring of multiple objects at once.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}

# SETTINGS

buttonx = "X"
buttony = "Y"
buttonz = "Z"
press = "PRESS"
ctrl = False
alt = True
shift = True


import bpy


class MultiMirrorMirrorX(bpy.types.Operator):
    bl_idname = "machin3.multi_mirror_mirrorx"
    bl_label = "MACHIN3: Multi Mirror Mirror X"

    def execute(self, context):
        multi_mirror_mirror(bpy.ops.object.mirror_mirror_x)
        return {'FINISHED'}


class MultiMirrorMirrorY(bpy.types.Operator):
    bl_idname = "machin3.multi_mirror_mirrory"
    bl_label = "MACHIN3: Multi Mirror Mirror Y"

    def execute(self, context):
        multi_mirror_mirror(bpy.ops.object.mirror_mirror_y)
        return {'FINISHED'}


class MultiMirrorMirrorZ(bpy.types.Operator):
    bl_idname = "machin3.multi_mirror_mirrorz"
    bl_label = "MACHIN3: Multi Mirror Mirror Z"

    def execute(self, context):
        multi_mirror_mirror(bpy.ops.object.mirror_mirror_z)
        return {'FINISHED'}


def multi_mirror_mirror(mirrormirrortool):
    activeobj = bpy.context.scene.objects.active
    selection = bpy.context.selected_objects
    selection.remove(activeobj)

    for obj in selection:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[obj.name].select = True
        bpy.data.objects[activeobj.name].select = True
        bpy.context.scene.objects.active = activeobj
        mirrormirrortool()

        # DECALmachine support (u mirror for parallax and for info decals!)
        if "decal" in obj.name or "info" in obj.name:
            for mod in obj.modifiers:
                if "mirror" in mod.name.lower():
                    mod.use_mirror_u = True

    for obj in selection:
        bpy.data.objects[obj.name].select = True
    bpy.data.objects[activeobj.name].select = True
    bpy.context.scene.objects.active = activeobj


def register():
    bpy.utils.register_class(MultiMirrorMirrorX)
    bpy.utils.register_class(MultiMirrorMirrorY)
    bpy.utils.register_class(MultiMirrorMirrorZ)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(MultiMirrorMirrorX.bl_idname, buttonx, press, ctrl=ctrl, alt=alt, shift=shift)
    kmi = km.keymap_items.new(MultiMirrorMirrorY.bl_idname, buttony, press, ctrl=ctrl, alt=alt, shift=shift)
    kmi = km.keymap_items.new(MultiMirrorMirrorZ.bl_idname, buttonz, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(MultiMirrorMirrorX)
    bpy.utils.unregister_class(MultiMirrorMirrorY)
    bpy.utils.unregister_class(MultiMirrorMirrorZ)

    # TODO: properly unregister keymap and keymap_items


if __name__ == "__main__":
    register()
