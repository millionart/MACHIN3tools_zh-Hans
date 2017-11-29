import bpy
from bpy.props import FloatProperty


class ClippingToggle(bpy.types.Operator):
    bl_idname = "machin3.clipping_toggle"
    bl_label = "MACHIN3: Clipping Toggle"
    bl_options = {'REGISTER', 'UNDO'}

    minimum = FloatProperty(name="Minimum", default=0.001)
    medium = FloatProperty(name="Medium", default=0.01)
    maximum = FloatProperty(name="Maximum", default=0.1)

    current = FloatProperty(name="Current")

    def execute(self, context):
        spaced = bpy.context.space_data

        # NOTE: there's small amounts added to the ranges to compensate for float imprecision

        if spaced.clip_start <= self.minimum + 0.0001:
            spaced.clip_start = self.medium
        elif self.minimum < spaced.clip_start <= self.medium + 0.001:
            spaced.clip_start = self.maximum
        else:
            spaced.clip_start = self.minimum

        self.current = spaced.clip_start
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.prop(self, "current")
        col.separator()

        col.prop(self, "minimum")
        col.prop(self, "medium")
        col.prop(self, "maximum")
