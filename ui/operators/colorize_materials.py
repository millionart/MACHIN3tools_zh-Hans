import bpy
from ... utils import MACHIN3 as m3


class ColorizeMaterials(bpy.types.Operator):
    bl_idname = "machin3.colorize_materials"
    bl_label = "Colorize Materials"
    bl_options = {'REGISTER', 'UNDO'}

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
                                    mat.diffuse_color = color.default_value[:3]

        return {'FINISHED'}
