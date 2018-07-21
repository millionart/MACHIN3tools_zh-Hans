import bpy
from bpy.props import StringProperty, IntProperty


class AppendMatsUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # isvisibleicon = "RESTRICT_VIEW_OFF" if item.isvisible else "RESTRICT_VIEW_ON"
        # islockedicon = "LOCKED" if item.islocked else "BLANK1"

        row = layout.split(0.7)
        row.label(text=item.name)

        # row = split.row()
        # row.label(text=item.name)
        # row = split.row()
        # row.prop(item, "isvisible", text="", icon=isvisibleicon, emboss=False)
        # row.prop(item, "islocked", text="", icon=islockedicon, emboss=False)


class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    # index: IntProperty()
