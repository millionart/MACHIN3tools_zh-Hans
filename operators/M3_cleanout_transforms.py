import bpy


class CleanoutTransforms(bpy.types.Operator):
    bl_idname = 'machin3.cleanout_transforms'
    bl_label = 'MACHIN3: Cleanout Transforms'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for t in context.scene.orientations:
            context.space_data.transform_orientation = t.name
            override = {'context': context,
                        'area': context.area,
                        'window': context.window,
                        'screen': context.screen,
                        'scene': context.scene,
                        'region': context.region,
                        'name': t.name}

            bpy.ops.transform.delete_orientation(override)
        bpy.context.space_data.transform_orientation = "NORMAL"
        return {"FINISHED"}
