import bpy
from bpy.props import BoolProperty, EnumProperty
from .. utils import MACHIN3 as m3


mode_items = [("FOCUS", "Focus", ""),
              ("LOCALVIEW", "Local View", "")]


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: 聚焦"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Mode", items=mode_items, default="FOCUS")

    view_selected: BoolProperty(name="查看选中项", default=True)
    unmirror: BoolProperty(name="非镜像", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "mode", expand=True)

        if self.mode == "FOCUS":
            row = column.row()
            row.prop(self, "view_selected")
            row.prop(self, "unmirror")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        # local view
        if self.mode == "LOCALVIEW":
            bpy.ops.view3d.localview(frame_selected=False)

        # focus
        elif self.mode == "FOCUS":
            history = context.scene.M3.focus_history

            sel = context.selected_objects

            if sel:
                self.focus(context, sel, history)


            elif history:
                self.unfocus(context, history)

            # for epoch in history:
                # print(epoch.name, ", hidden: ", [obj.name for obj in epoch.objects], ", unmirrored: ", [obj.name for obj in epoch.unmirrored])

        return {'FINISHED'}

    def focus(self, context, sel, history):
        hidden = []
        visible = context.visible_objects

        # hide objects not in the selection (and not already hidden)

        for obj in visible:
            if obj not in sel:
                hidden.append(obj)
                obj.hide_viewport = True

        # create new epoch, if objects were hidden

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
                    mirrored = [(obj, mod) for mod in obj.modifiers if mod.type == "MIRROR"]

                    for mobj, mod in mirrored:
                        if mod.show_viewport:
                            mod.show_viewport = False

                            entry = epoch.unmirrored.add()
                            entry.obj = mobj
                            entry.name = mobj.name

            # view selected

        if self.view_selected:
            bpy.ops.view3d.view_selected()

    def unfocus(self, context, history):
        selected = []
        visible = context.visible_objects

        # for view_selected, select visible objects

        if self.view_selected:

            for obj in visible:
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
