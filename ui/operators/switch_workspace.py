import bpy
from bpy.props import StringProperty


class SwitchWorkspace(bpy.types.Operator):
    bl_idname = "machin3.switch_workspace"
    bl_label = "Switch Workspace"
    bl_options = {'REGISTER'}

    name: StringProperty()

    def execute(self, context):

        # get current workspace
        ws = bpy.data.workspaces.get(self.name)

        # get view matrix from 3d view (if present)
        viewmx = self.get_view_matrix(context, ws)

        # if the chosen workspace is already active, select the alternative one, if present
        if ws and context.window.workspace == ws:
            ws = bpy.data.workspaces.get('%s.alt' % self.name)

            if ws:
                bpy.context.window.workspace = ws

        # otherwise just switch to the chosen one
        elif ws:
                bpy.context.window.workspace = ws

        # set previous view matrix to new view
        if viewmx:
            self.set_view_matrix(ws, viewmx)

        return {'FINISHED'}

    def set_view_matrix(self, workspace, viewmx):
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            r3d = space.region_3d
                            r3d.view_matrix = viewmx
                            return

    def get_view_matrix(self, context, workspace):
        if context.space_data.type == 'VIEW_3D':
            return context.space_data.region_3d.view_matrix
