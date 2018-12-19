import bpy
from bpy.props import StringProperty, EnumProperty
from ... utils.registration import get_prefs
from ... utils import MACHIN3 as m3


# TODO: populste world and materials automatically, using bpy.data.labraries.load

def get_mat():
    idx = get_prefs().appendmatsIDX
    mats = get_prefs().appendmats
    active = mats[idx]

    return idx, mats, active


class Add(bpy.types.Operator):
    bl_idname = "machin3.add_appendmat"
    bl_label = "Add Append Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add name of Material to append"

    @classmethod
    def poll(cls, context):
        name = get_prefs().appendmatsname
        appendmats = get_prefs().appendmats

        return name and name not in appendmats

    def execute(self, context):
        name = get_prefs().appendmatsname
        appendmats = get_prefs().appendmats

        if name not in appendmats:
            am = appendmats.add()
            am.name = name

            appendmats = get_prefs().appendmatsname = ""

        return {'FINISHED'}


class Move(bpy.types.Operator):
    bl_idname = "machin3.move_appendmat"
    bl_label = "Move Material Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Move Material Name up or down.\nThis controls the position in the Append Material Menu.\nSave prefs to remember."

    direction: EnumProperty(items=[("UP", "Up", ""),
                                   ("DOWN", "Down", "")])

    def execute(self, context):
        idx, mats, _ = get_mat()

        if self.direction == "UP":
            nextidx = max(idx - 1, 0)
        elif self.direction == "DOWN":
            nextidx = min(idx + 1, len(mats) - 1)

        mats.move(idx, nextidx)
        get_prefs().appendmatsIDX = nextidx

        return {'FINISHED'}


class Rename(bpy.types.Operator):
    bl_idname = "machin3.rename_appendmat"
    bl_label = "Rename Material Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Rename the selected Material Name"

    newmatname: StringProperty(name="New Name")

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        # row = column.split(percentage=0.31)
        # row.label("Old Name")
        # row.label(self.active.name)

        column.prop(self, "newmatname")

    def invoke(self, context, event):
        _, _, self.active = get_mat()

        self.newmatname = self.active.name

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        if self.newmatname:
            self.active.name = self.newmatname

        return {'FINISHED'}


class Clear(bpy.types.Operator):
    bl_idname = "machin3.clear_appendmats"
    bl_label = "Clear All Material Names"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Clear All Material Names.\nSave prefs to remember."

    def execute(self, context):
        get_prefs().appendmats.clear()

        return {'FINISHED'}


class Remove(bpy.types.Operator):
    bl_idname = "machin3.remove_appendmat"
    bl_label = "Remove Material Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove selected Material Name.\nSave prefs to remember."

    def execute(self, context):
        idx, mats, _ = get_mat()

        mats.remove(idx)
        return {'FINISHED'}
