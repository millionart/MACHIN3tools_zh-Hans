import bpy
from bpy.props import BoolProperty
from .. import M3utils as m3


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"
    bl_options = {'REGISTER', 'UNDO'}

    isolate = BoolProperty(name="Isolate (Local View)", default=False)
    mirror = BoolProperty(name="Toggle Mirror", default=True)

    def draw(self, context):
        layout = self.layout
        column = layout.column()

    def execute(self, context):
        if self.isolate:
            localview = self.get_localview()
            if not localview:  # entering focus mode(local view)
                self.toggle_mirror()
                bpy.ops.view3d.localview()
            else:  # leaving focus mode(local view)
                m3.select_all("OBJECT")
                self.toggle_mirror()
                bpy.ops.view3d.localview()
        else:
            sel = m3.selected_objects()

            if len(sel) == 1 and self.mirror:
                    self.toggle_mirror()

            bpy.ops.view3d.view_selected(use_all_regions=False)

            if len(sel) == 1 and self.mirror:
                self.toggle_mirror()

        return {'FINISHED'}

    def toggle_mirror(self):
        for obj in bpy.context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == "MIRROR":
                    mod.show_viewport = not mod.show_viewport

    def get_localview(self):
        localview = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                if area.spaces.active.local_view is not None:
                    localview = True
        return localview
