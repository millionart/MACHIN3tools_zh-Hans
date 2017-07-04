import bpy


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        localview = self.get_localview()
        if not localview:  # entering focus mode(local view)
            self.turn_mirror("OFF")
            bpy.ops.view3d.localview()
        else:  # leaving focus mode(local view)
            self.turn_mirror("ON")
            bpy.ops.view3d.localview()
        return {'FINISHED'}

    def turn_mirror(self, string):
        for obj in bpy.context.selected_objects:
            for mod in obj.modifiers:
                if "mirror" in mod.name.lower():
                    # print("Found mirror: %s" % (mod.name))
                    if string == "OFF":
                        mod.show_viewport = False
                    elif string == "ON":
                        mod.show_viewport = True

    def get_localview(self):
        localview = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                if area.spaces.active.local_view is not None:
                    localview = True
        return localview
