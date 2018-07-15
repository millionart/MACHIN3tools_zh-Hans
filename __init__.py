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
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.utils import register_class, unregister_class
from . utils import MACHIN3 as m3


# TODO: add automatic custom blender keymaps option
# TODO: OSD feedback, so you dont have to check into the op props to verify a tool did what you want it to do


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)

    pieobjecteditmodehide = BoolProperty(name="Auto Hide", default=False)
    pieobjecteditmodeshow = BoolProperty(name="Auto Reveal", default=False)
    pieobjecteditmodeshowunselect = BoolProperty(name="Unselect", default=False)
    pieobjecteditmodetoggleao = BoolProperty(name="Toggle AO", default=False)

    pieviewsalignactive = bpy.props.BoolProperty(name="Align Active", default=False)

    preview_percentage = IntProperty(name="Preview Percentage", default=100, min=10, max=100, subtype="PERCENTAGE")
    final_percentage = IntProperty(name="Final Percentage", default=250, min=100, max=1000, subtype="PERCENTAGE")

    preview_samples = IntProperty(name="Preview Percentage", default=32, min=12, max=64)
    final_samples = IntProperty(name="Final Percentage", default=256, min=64, max=2048)



preferences_tabs = [("MODULES", "Modules", ""),
                    ("SPECIALMENUS", "Special Menus", ""),
                    ("PIEMENUS", "Pie Menus", ""),
                    ("CUSTOMKEYS", "Custom Keys", "")]


class MACHIN3Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    M3path = __path__[0]

    # TABS

    tabs = EnumProperty(name="Tabs", items=preferences_tabs, default="MODULES")


    def draw(self, context):
        layout=self.layout

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = column.box()

        # if self.tabs == "MODULES":
            # self.draw_modules(box, kc)
        # elif self.tabs == "SPECIALMENUS":
            # self.draw_special(box, kc)
        # elif self.tabs == "PIEMENUS":
            # self.draw_pies(box, kc)



def register_pie_keys(wm, keymaps):
    # SELECT MODE

    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_select_modes"
    kmi.active = True
    keymaps.append((km, kmi))




def get_classes():
    from . ui.pie import PieSelectMode
    from . ui.operators.select_modes import SelectVertexMode, SelectEdgeMode, SelectFaceMode, SelectEditObjectMode


    classes = []

    # pie menus

    classes.append(PieSelectMode)
    classes.append(SelectVertexMode)
    classes.append(SelectEdgeMode)
    classes.append(SelectFaceMode)
    classes.append(SelectEditObjectMode)

    return classes


keymaps = []
classes = get_classes()


def register():
    # CLASSES
    for c in classes:
        register_class(c)

    wm = bpy.context.window_manager

    # PIE MENUS  KEYS

    register_pie_keys(wm, keymaps)


def unregister():
    # CLASSES
    for c in classes:
        unregister_class(c)


    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)

    keymaps.clear()
