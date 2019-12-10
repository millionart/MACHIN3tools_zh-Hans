import bpy
from ... utils.draw import add_object_axes_drawing_handler, remove_object_axes_drawing_handler


class ToggleObjectAxes(bpy.types.Operator):
    bl_idname = "machin3.toggle_object_axes"
    bl_label = "MACHIN3: Toggle Object Axes"
    bl_description = "Show local axes on objects in selection, or all visible objects if nothing is selected"
    bl_options = {'REGISTER'}

    def execute(self, context):
        dns = bpy.app.driver_namespace
        handler = dns.get('draw_object_axes')

        if handler:
            remove_object_axes_drawing_handler(handler)

        else:
            objs = [obj for obj in context.selected_objects] if context.selected_objects else context.visible_objects

            if objs:
                args = (context, objs)
                add_object_axes_drawing_handler(dns, args)

        context.area.tag_redraw()
        return {'FINISHED'}
