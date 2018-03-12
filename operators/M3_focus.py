import bpy
from bpy.props import BoolProperty, IntProperty
from .. import M3utils as m3


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"

    isolate = BoolProperty(name="Isolate (Local View)", default=False)
    mirror = BoolProperty(name="Toggle Mirror", default=False)
    zoomout = IntProperty(name="Zoom Out after Focus", default=0)

    def execute(self, context):
        if self.isolate:
            localview = self.get_localview()
            if not localview:  # entering focus mode(local view)
                if self.mirror:
                    self.toggle_mirror()
                bpy.ops.view3d.localview()
                # bpy.ops.view3d.localview('INVOKE_DEFAULT')  # this has the animation, but won't do the zoomout

                for z in range(self.zoomout):
                    bpy.ops.view3d.zoom(delta=-1)

            else:  # leaving focus mode(local view)
                m3.unhide_all("OBJECT")
                m3.select_all("OBJECT")
                if self.mirror:
                    self.toggle_mirror()
                # bpy.ops.view3d.localvie()
                bpy.ops.view3d.localview('INVOKE_DEFAULT')
        else:
            mode = m3.get_mode()

            if mode == "OBJECT":
                sel = m3.selected_objects()

                if len(sel) == 1 and self.mirror:
                        self.toggle_mirror()

                bpy.ops.view3d.view_selected(use_all_regions=False)

                for z in range(self.zoomout):
                    bpy.ops.view3d.zoom(delta=-1)

                if len(sel) == 1 and self.mirror:
                    self.toggle_mirror()
            else:
                bpy.ops.view3d.view_selected('INVOKE_DEFAULT', use_all_regions=False)

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
