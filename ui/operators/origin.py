import bpy
from bpy.props import BoolProperty
from ... utils.object import parent, unparent


class OriginToActive(bpy.types.Operator):
    bl_idname = "machin3.origin_to_active"
    bl_label = "MACHIN3: Origin to Active"
    bl_description = "Set Selected Objects' Origin to Active Object"
    bl_options = {'REGISTER', 'UNDO'}

    skip_children: BoolProperty(name="Parents", description="Don't transform children", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        column.prop(self, "skip_children", toggle=True)

    @classmethod
    def poll(cls, context):
        if context.mode == 'OBJECT':
            active = context.active_object
            sel = [obj for obj in context.selected_objects if obj != active]
            return active and sel

    def execute(self, context):
        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        mx = active.matrix_world

        for obj in sel:
            if self.skip_children:
                children = self.unparent_children(obj.children)

            omx = obj.matrix_world.copy()

            obj.data.transform(mx.inverted() @ omx)
            obj.matrix_world = mx
            obj.data.update()

            if self.skip_children:
                self.reparent_children(children, obj)

        return {'FINISHED'}

    def unparent_children(self, children):
        children = [o for o in children]

        for c in children:
            unparent(c)

        return children

    def reparent_children(self, children, obj):
        for c in children:
            parent(c, obj)
