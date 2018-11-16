import bpy
from bpy.props import FloatProperty
from ... utils import MACHIN3 as m3


# TODO: unique preset colors for decal types

class ColorizeMaterials(bpy.types.Operator):
    bl_idname = "machin3.colorize_materials"
    bl_label = "Colorize Materials"
    bl_options = {'REGISTER', 'UNDO'}

    lighten_amount: FloatProperty(name="Lighten", default=0.05, min=0, max=1)

    @classmethod
    def poll(cls, context):
        return bpy.data.materials

    def execute(self, context):
        for mat in bpy.data.materials:
            if mat.use_nodes:
                tree = mat.node_tree
                output = tree.nodes.get("Material Output")
                if output:
                    surf = output.inputs.get("Surface")
                    if surf:
                        if surf.links:
                            node = surf.links[0].from_node

                            if node:
                                color = node.inputs.get("Base Color")

                                if not color:
                                    color = node.inputs.get("Color")

                                if color:
                                    mat.diffuse_color = self.lighten(color=color.default_value[:3], amount=self.lighten_amount)

        return {'FINISHED'}

    def lighten(self, color, amount):
        return tuple(remap(c, amount) for c in color)



def remap(value, new_low):
    old_range = (1 - 0)
    new_range = (1 - new_low)
    return (((value - 0) * new_range) / old_range) + new_low
