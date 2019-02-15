import bpy
from bpy.props import FloatProperty


class ClippingToggle(bpy.types.Operator):
    bl_idname = "machin3.clipping_toggle"
    bl_label = "MACHIN3: 剪切切换"
    bl_options = {'REGISTER', 'UNDO'}

    maximum: FloatProperty(name="最大值", default=0.1, min=0)
    medium: FloatProperty(name="中间值", default=0.01, min=0)
    minimum: FloatProperty(name="最小值", default=0.001, min=0)

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
