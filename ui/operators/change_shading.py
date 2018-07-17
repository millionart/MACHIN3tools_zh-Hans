import bpy
from ... utils import MACHIN3 as m3



solid_show_overlays = True
material_show_overlays = False
rendered_show_overlays = False


class ShadeSolid(bpy.types.Operator):
    bl_idname = "machin3.shade_solid"
    bl_label = "Shade Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global solid_show_overlays

        # toggle overlays
        if context.space_data.shading.type == 'SOLID':
            solid_show_overlays = not solid_show_overlays
            bpy.context.space_data.overlay.show_overlays = solid_show_overlays

        # change shading to SOLID 
        else:
            context.space_data.shading.type = 'SOLID'
            bpy.context.space_data.overlay.show_overlays = solid_show_overlays

        return {'FINISHED'}


class ShadeMaterial(bpy.types.Operator):
    bl_idname = "machin3.shade_material"
    bl_label = "Shade Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global material_show_overlays

        # toggle overlays
        if context.space_data.shading.type == 'MATERIAL':
            material_show_overlays = not material_show_overlays
            bpy.context.space_data.overlay.show_overlays = material_show_overlays

        # change shading to MATERIAL
        else:
            context.space_data.shading.type = 'MATERIAL'
            bpy.context.space_data.overlay.show_overlays = material_show_overlays

        return {'FINISHED'}


class ShadeRendered(bpy.types.Operator):
    bl_idname = "machin3.shade_rendered"
    bl_label = "Shade Rendered"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global rendered_show_overlays

        # toggle overlays
        if context.space_data.shading.type == 'RENDERED':
            rendered_show_overlays = not rendered_show_overlays
            bpy.context.space_data.overlay.show_overlays = rendered_show_overlays

        # change shading to RENDERED
        else:
            context.space_data.shading.type = 'RENDERED'
            bpy.context.space_data.overlay.show_overlays = rendered_show_overlays

        return {'FINISHED'}
