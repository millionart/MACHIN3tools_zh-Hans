import bpy
from bpy.props import IntProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper


class QuadSphere(bpy.types.Operator):
    bl_idname = "machin3.quadsphere"
    bl_label = "MACHIN3: Quadsphere"
    bl_description = "Creates a Quadsphere"
    bl_options = {'REGISTER', 'UNDO'}

    subdivisions: IntProperty(name='Subdivisions', default=4, min=1, max=8)

    align_rotation: BoolProperty(name="Align Rotation", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "subdivisions")
        row.prop(self, "align_rotation", toggle=True)

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(align='CURSOR' if self.align_rotation else 'WORLD')

        mode = bpy.context.mode

        if mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')

        for sub in range(self.subdivisions):
            bpy.ops.mesh.subdivide(number_cuts=1, smoothness=1)
            bpy.ops.transform.tosphere(value=1)

        return {'FINISHED'}
