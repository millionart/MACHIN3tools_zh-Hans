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
        shading = self.get_shading(context, ws)

        # if the chosen workspace is already active, select the alternative one, if present and set the shading
        if ws and context.window.workspace == ws:
            ws = bpy.data.workspaces.get('%s.alt' % self.name)

            if ws:
                bpy.context.window.workspace = ws
                self.set_shading(ws, shading)

        # switch back to original(non-alt workspace) and set shading
        elif ws and ws.name + ".alt" == context.workspace.name:
            bpy.context.window.workspace = ws
            self.set_shading(ws, shading)

        # otherwise just switch to the chosen one, and don't set shading
        elif ws:
            bpy.context.window.workspace = ws

        # set previous view matrix to new view
        if ws and viewmx:
            self.set_view_matrix(ws, viewmx)

        return {'FINISHED'}

    def set_shading(self, workspace, shading):
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = shading[0]
                            space.shading.studio_light = shading[1]
                            space.shading.use_scene_lights = shading[2]
                            space.shading.use_scene_world = shading[3]

                            space.overlay.show_overlays = shading[4]
                            return

    def get_shading(self, context, workspace):
        if context.space_data.type == 'VIEW_3D':
            shading = context.space_data.shading

            shading_type = shading.type
            studio_light = shading.studio_light
            use_scene_lights = shading.use_scene_lights
            use_scene_world = shading.use_scene_world

            show_overlays = context.space_data.overlay.show_overlays


            return shading_type, studio_light, use_scene_lights, use_scene_world, show_overlays

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
