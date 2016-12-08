bl_info = {
    "name": "Center Cube",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu/Shift+C",
    "description": "If nothing is selected, places a cube at the cursor location, but with X zeroed, enters edit mode, selects all and initiates the scale tool. If objects are selcted, it zeroes out x.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}

button = "C"
press = "PRESS"
ctrl = False
alt = False
shift = True


import bpy


class CenterCube(bpy.types.Operator):
    bl_idname = "machin3.center_cube"
    bl_label = "MACHIN3: Center Cube"

    def execute(self, context):
        if len(bpy.context.selected_objects) == 0:  # no object selected
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            bpy.context.object.location[0] = 0
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.resize('INVOKE_DEFAULT', constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        else:  # objects selected
            for obj in bpy.context.selected_objects:
                bpy.context.scene.objects.active = obj
                bpy.context.object.location[0] = 0
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CenterCube)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new(CenterCube.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(CenterCube)

if __name__ == "__main__":
    register()
