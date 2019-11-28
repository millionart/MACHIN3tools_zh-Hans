import bpy
from bpy.props import StringProperty


class SwitchWorkspace(bpy.types.Operator):
    bl_idname = "machin3.switch_workspace"
    bl_label = "Switch Workspace"
    bl_options = {'REGISTER'}

    name: StringProperty()

    def execute(self, context):
        ws = bpy.data.workspaces.get(self.name)

        # if the chosen workspace is already active, select the alternative one, if present
        if ws and context.window.workspace == ws:
            ws = bpy.data.workspaces.get('%s.alt' % self.name)

            if ws:
                bpy.context.window.workspace = ws

        # otherwise just switch to the chosen one
        elif ws:
                bpy.context.window.workspace = ws

        return {'FINISHED'}
