import bpy
from .. utils import MACHIN3 as m3


# TODO: the mirror stuff

class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        history = context.scene.M3.focus_history

        sel = m3.selected_objects()

        if sel:
            self.focus(context, sel, history)

        elif history:
            self.unfocus(context, history)

        # for epoch in history:
            # print(epoch.name, ": ", [obj.name for obj in epoch.objects])

        return {'FINISHED'}

    def focus(self, context, sel, history):
        hidden = []

        for obj in context.view_layer.objects:
            if not obj.hide_viewport and obj not in sel:
                hidden.append(obj)
                obj.hide_viewport = True

        if hidden:
            epoch = history.add()
            epoch.name = "Epoch %d" % (len(history) - 1)

            for obj in hidden:
                entry = epoch.objects.add()
                entry.obj = obj
                entry.name = obj.name


    def unfocus(self, context, history):
        last_epoch = history[-1]

        for entry in last_epoch.objects:
            entry.obj.hide_viewport = False

        idx = history.keys().index(last_epoch.name)

        history.remove(idx)
