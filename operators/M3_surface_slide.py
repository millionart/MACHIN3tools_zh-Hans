import bpy
from .. import M3utils as m3


# TODO: needs visual representation that you are in slide mode and how to exit

class SurfaceSlide(bpy.types.Operator):
    bl_idname = "machin3.surface_slide"
    bl_label = "MACHIN3: Surface Slide"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        mode = m3.get_mode()
        active = m3.get_active()

        if mode != "OBJECT":
            surfacesrc = active.copy()
            surfacesrc.data = active.data.copy()
            surfacesrc.name = "surfacesrc_" + active.name

            self.shrinkwrap = active.modifiers.new(name="SurfaceSlide", type="SHRINKWRAP")
            self.shrinkwrap.target = surfacesrc
            self.shrinkwrap.show_on_cage = True

            bpy.ops.transform.translate("INVOKE_DEFAULT")

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in ['ESC', 'SPACE']:
            self.execute(context)
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        m3.set_mode("OBJECT")
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=self.shrinkwrap.name)
        bpy.data.objects.remove(self.shrinkwrap.target, do_unlink=True)

        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
