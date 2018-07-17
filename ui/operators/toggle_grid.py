import bpy
from ... utils import MACHIN3 as m3


axis_x = True
axis_y = True
axis_z = False


class ToggleGrid(bpy.types.Operator):
    bl_idname = "machin3.toggle_grid"
    bl_label = "Toggle Grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global axis_x, axis_y, axis_z

        overlay = context.space_data.overlay

        grid = context.space_data.overlay.show_floor

        if grid:
            # get axes states
            axis_x = overlay.show_axis_x
            axis_y = overlay.show_axis_y
            axis_z = overlay.show_axis_z

            # turn grid OFF
            overlay.show_floor = False

            # turn axes OFF
            overlay.show_axis_x = False
            overlay.show_axis_y = False
            overlay.show_axis_z = False

        else:
            # turn grid ON
            overlay.show_floor = True

            # turn axes ON (according to previous states)
            overlay.show_axis_x = axis_x
            overlay.show_axis_y = axis_y
            overlay.show_axis_z = axis_z

        return {'FINISHED'}
