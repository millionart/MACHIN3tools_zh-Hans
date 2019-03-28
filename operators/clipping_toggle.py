import bpy
from bpy.props import FloatProperty


class ClippingToggle(bpy.types.Operator):
    bl_idname = "machin3.clipping_toggle"
    bl_label = "MACHIN3: Clipping Toggle"
    bl_options = {'REGISTER', 'UNDO'}

    maximum: FloatProperty(name="Maximum", default=0.1, min=0, precision=1)
    medium: FloatProperty(name="Medium", default=0.01, min=0, precision=2)
    minimum: FloatProperty(name="Minimum", default=0.001, min=0, precision=3)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row(align=True)

        row.prop(self, "minimum", text="Min")
        row.prop(self, "medium", text="Med")
        row.prop(self, "maximum", text="Max")

    def execute(self, context):
        view = bpy.context.space_data

        if view.clip_start >= self.maximum:
            view.clip_start = self.medium

        elif view.clip_start >= self.medium:
            view.clip_start = self.minimum

        else:
            view.clip_start = self.maximum

        return {'FINISHED'}
