'''
Copyright (C) 2017 MACHIN3, machin3.io, support@machin3.io

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


bl_info = {
    "name": "MACHIN3tools",
    "author": "MACHIN3",
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "",
    "description": "A collection of blender python scripts.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, PointerProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from . classes import get_classes
from . keymaps import register_keymaps
from . properties import AppendMatsCollection, AppendMatsUIList, M3SceneProperties
from . icons import register_icons, unregister_icons, get_icon



# TODO: OSD feedback, so you dont have to check into the op props to verify a tool did what you want it to do


preferences_tabs = [("MODULES", "Modules", ""),
                    ("SPECIALMENUS", "Special Menus", ""),
                    ("PIEMENUS", "Pie Menus", ""),
                    ("CUSTOMKEYS", "Custom Keys", "")]


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    M3path = __path__[0]

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.user_preferences.studio_lights if "datafiles/studiolights/matcap" in mc.path]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "NOT FOUND"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.user_preferences.studio_lights if "datafiles/studiolights/matcap" in mc.path]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "NOT FOUND"


    # MACHIN3pies

    appendworldpath: StringProperty(name="Append World from", subtype='FILE_PATH')
    appendworldname: StringProperty(name="Name of World to append")

    appendmatspath: StringProperty(name="Append Materials from", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty()


    switchmatcap1: StringProperty(name="Matcap 1", update=update_switchmatcap1)
    switchmatcap2: StringProperty(name="Matcap 2", update=update_switchmatcap2)


    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="Activate Smart Vert", default=False)

    # hidden

    avoid_update: BoolProperty(default=False)


    # TABS

    # tabs = EnumProperty(name="Tabs", items=preferences_tabs, default="MODULES")

    def draw(self, context):
        layout=self.layout

        # wm = bpy.context.window_manager
        # kc = wm.keyconfigs.user


        # column = layout.column(align=True)
        # row = column.row()
        # row.prop(self, "tabs", expand=True)

        # box = column.box()


        # if self.tabs == "MODULES":
            # self.draw_modules(box, kc)
        # elif self.tabs == "SPECIALMENUS":
            # self.draw_special(box, kc)
        # elif self.tabs == "PIEMENUS":
            # self.draw_pies(box, kc)


        box = layout.box()
        split = box.split()

        # APPEND WORLD AND MATERIALS

        b = split.box()
        column = b.column()

        column.prop(self, "appendworldpath")
        column.prop(self, "appendworldname")
        column.separator()

        column.prop(self, "appendmatspath")


        column = b.column()

        row = column.row()
        rows = len(self.appendmats) if len(self.appendmats) > 6 else 6
        row.template_list("AppendMatsUIList", "", self, "appendmats", self, "appendmatsIDX", rows=rows)

        c = row.column(align=True)
        c.operator("machin3.move_appendmat", text="", icon='TRIA_UP').direction = "UP"
        c.operator("machin3.move_appendmat", text="", icon='TRIA_DOWN').direction = "DOWN"

        c.separator()
        c.separator()
        c.operator("machin3.rename_appendmat", text="", icon='OUTLINER_DATA_FONT')
        c.separator()
        c.separator()
        c.operator("machin3.clear_appendmats", text="", icon='LOOP_BACK')
        c.operator("machin3.remove_appendmat", text="", icon_value=get_icon('cancel'))

        row = column.row()
        row.prop(self, "appendmatsname")
        row.operator("machin3.add_appendmat", text="", icon_value=get_icon('plus'))


        # MATCAP SWITCH

        column.separator()
        row = column.row()

        row.prop(self, "switchmatcap1")
        row.prop(self, "switchmatcap2")


        b = split.box()

        # MACHIN3tools

        column = b.column()

        column.prop(self, "activate_smart_vert")



classes = [AppendMatsUIList, AppendMatsCollection, MACHIN3toolsPreferences, M3SceneProperties]


def register():
    global classes, keymaps

    classes = get_classes(classes)

    # CLASSES

    for c in classes:
        register_class(c)

    # PROPERTIES

    bpy.types.Scene.M3 = PointerProperty(type=M3SceneProperties)


    # KEYMAPS

    keymaps = register_keymaps()

    register_icons()


def unregister():
    global classes, keymaps

    # CLASSES

    for c in classes:
        unregister_class(c)

    # KEYMAPS

    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)

    keymaps.clear()
