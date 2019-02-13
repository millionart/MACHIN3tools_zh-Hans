import bpy
from bpy.props import FloatProperty
from ... utils import MACHIN3 as m3
from ... utils.material import get_last_node, lighten_color


# TODO: unique preset colors for decal types

class ColorizeMaterials(bpy.types.Operator):
    bl_idname = "machin3.colorize_materials"
    bl_label = "MACHIN3: Colorize Materials"
    descriptino = "Set Material Viewport Colors from last Node in Materials"
    bl_options = {'REGISTER', 'UNDO'}

    lighten_amount: FloatProperty(name="Lighten", default=0.05, min=0, max=1)

    @classmethod
    def poll(cls, context):
        return bpy.data.materials

    def execute(self, context):
        for mat in bpy.data.materials:
            node = get_last_node(mat)

            if node:
                color = node.inputs.get("Base Color")

                if not color:
                    color = node.inputs.get("Color")

                if color:
                    mat.diffuse_color = lighten_color(color=color.default_value, amount=self.lighten_amount)

        return {'FINISHED'}


class ColorizeObjectsFromMaterials(bpy.types.Operator):
    bl_idname = "machin3.colorize_objects_from_materials"
    bl_label = "MACHIN3: Colorize Objects from Materials"
    bl_description = "Set Object Viewport Colors of selected Objects from their active Materials"
    bl_options = {'REGISTER', 'UNDO'}

    lighten_amount: FloatProperty(name="Lighten", default=0.05, min=0, max=1)

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        for obj in context.selected_objects:
            mat = obj.active_material

            if mat:
                node = get_last_node(mat)

                if node:
                    color = node.inputs.get("Base Color")

                    if not color:
                        color = node.inputs.get("Color")

                    if color:
                        obj.color = lighten_color(color=color.default_value, amount=self.lighten_amount)

        return {'FINISHED'}


class ColorizeObjectsFromActive(bpy.types.Operator):
    bl_idname = "machin3.colorize_objects_from_active"
    bl_label = "MACHIN3: Colorize Objects from Active"
    bl_description = "Set Object Viewport Colors from Active Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.selected_objects

    def execute(self, context):
        activecolor = context.active_object.color

        for obj in context.selected_objects:
            obj.color = activecolor

        return {'FINISHED'}
