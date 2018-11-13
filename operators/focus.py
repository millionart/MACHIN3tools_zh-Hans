import bpy
from bpy.props import BoolProperty
from .. utils import MACHIN3 as m3


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"
    bl_options = {'REGISTER', 'UNDO'}

    view_selected: BoolProperty(name="View Selcted", default=True)
    unmirror: BoolProperty(name="Un-Mirror", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "view_selected")
        row.prop(self, "unmirror")


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

        # hide objects not in the selection (and not already hidden)

        for obj in context.view_layer.objects:
            if not obj.hide_viewport and obj not in sel:
                hidden.append(obj)
                obj.hide_viewport = True

        # create new epoch, if there are objects to hide

        if hidden:
            epoch = history.add()
            epoch.name = "Epoch %d" % (len(history) - 1)

            # store hidden objects

            for obj in hidden:
                entry = epoch.objects.add()
                entry.obj = obj
                entry.name = obj.name

            # disable mirror mods and store these unmirrored objects

            if self.unmirror:
                for obj in sel:
                    for mod in obj.modifiers:
                        if mod.type == "MIRROR":
                            if mod.show_viewport:
                                mod.show_viewport = False

                                entry = epoch.unmirrored.add()
                                entry.obj = obj
                                entry.name = obj.name

            # view selected

            if self.view_selected:
                bpy.ops.view3d.view_selected()

    def unfocus(self, context, history):
        selected = []

        # for view_selected, select visible objects

        if self.view_selected:

            for obj in context.view_layer.objects:
                if not obj.hide_viewport:
                    obj.select_set(True)
                    selected.append(obj)

        last_epoch = history[-1]

        # restore hidden objects and select them

        for entry in last_epoch.objects:
            entry.obj.hide_viewport = False

            if self.view_selected:
                entry.obj.select_set(True)
                selected.append(entry.obj)

        # re-enbable mirror mods

        if self.unmirror:
            for entry in last_epoch.unmirrored:
                for mod in entry.obj.modifiers:
                    if mod.type == "MIRROR":
                        mod.show_viewport = True

        # delete the last epoch

        idx = history.keys().index(last_epoch.name)

        history.remove(idx)

        # view selected and deselect everythng

        if self.view_selected:
            bpy.ops.view3d.view_selected()

            for obj in selected:
                obj.select_set(False)
