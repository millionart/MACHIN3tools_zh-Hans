import bpy
import bgl
import blf
from .. import M3utils as m3

# NOTE: escaping out of an invoked move command will crash blender

class SurfaceSlide(bpy.types.Operator):
    bl_idname = "machin3.surface_slide"
    bl_label = "MACHIN3: Surface Slide"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        mode = m3.get_mode()
        active = m3.get_active()
        shrinkwrap = active.modifiers.get("SurfaceSlide")

        if mode != "OBJECT":
            # mark the current mesh state in the undo stack
            # without this canceling a SurfaceSlide would undo all mesh operations done before SurfaceSlide was called
            m3.set_mode("OBJECT")
            bpy.ops.ed.undo_push(message="MACHIN3: Pre-SurfaceSlide-State")
            m3.set_mode("EDIT")

            if shrinkwrap is None:  # prevent it beeling called while it's already active

                args = (self, context)

                self.handle = bpy.types.SpaceView3D.draw_handler_add(draw_overlays, args, 'WINDOW', 'POST_PIXEL')

                self.surfacesrc = active.copy()
                self.surfacesrc.data = active.data.copy()
                self.surfacesrc.name = "surfacesrc_" + active.name

                shrinkwrap = active.modifiers.new(name="SurfaceSlide", type="SHRINKWRAP")
                shrinkwrap.target = self.surfacesrc
                shrinkwrap.show_on_cage = True

                while active.modifiers[0].name != "SurfaceSlide":
                    bpy.ops.object.modifier_move_up(modifier="SurfaceSlide")

                bpy.ops.transform.translate("INVOKE_DEFAULT")

                context.window_manager.modal_handler_add(self)
            else:
                bpy.ops.transform.translate("INVOKE_DEFAULT")

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.header_text_set("MACHIN3: SurfaceSlide - ESC: cancel, SPACE: confirm")
        context.area.tag_redraw()

        if event.type in ['SPACE']:
            bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')
            self.confirm(context)
            return {'FINISHED'}
        if event.type in ['ESC']:
            bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')
            self.cancel(context)
            # return {'FINISHED'}
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def confirm(self, context):
        context.area.header_text_set()
        m3.set_mode("OBJECT")
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="SurfaceSlide")
        bpy.data.objects.remove(self.surfacesrc, do_unlink=True)
        bpy.ops.ed.undo_push(message="MACHIN3: Surface Slide")
        bpy.ops.object.editmode_toggle()

    def cancel(self, context):
        context.area.header_text_set()
        m3.set_mode("OBJECT")  # this is causing the crash when escaping out of the move tool after starting surface slide(with a selection)

        # manually push the undo state, otherwise you can't undo as the operator is still unfinished
        bpy.ops.ed.undo_push(message="MACHIN3: Surface Slide")
        bpy.ops.ed.undo()
        bpy.data.objects.remove(self.surfacesrc, do_unlink=True)
        bpy.ops.object.modifier_remove(modifier="SurfaceSlide")
        bpy.ops.object.editmode_toggle()


def draw_overlays(self, context):
    region = context.region
    draw_border(self, context)
    draw_text(self, context, text="Surface Slide", size=20, x=region.width - 140, y=30)
    draw_text(self, context, text="SPACE to confirm, ESC to cancel", size=12, x=region.width - 188, y=13)


def draw_text(self, context, text="ABC123", size=16, x=0, y=0):
    font_id = 0

    blf.position(font_id, x, y, 0)
    bgl.glColor4f(1, 1, 1, 0.75)
    blf.size(font_id, size, 72)
    blf.draw(font_id, text)


def draw_border(self, context):
    region = context.region

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glColor4f(1, 1, 1, 0.75)
    lw = 2
    bgl.glLineWidth(lw)

    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2i(lw, lw)
    bgl.glVertex2i(region.width - lw, lw)
    bgl.glVertex2i(region.width - lw, region.height - lw)
    bgl.glVertex2i(lw, region.height - lw)
    bgl.glVertex2i(lw, lw)
    bgl.glEnd()
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)
