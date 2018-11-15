'''
Copyright (C) 2018 MACHIN3, machin3.io, support@machin3.io

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
    "description": "A collection of Blender tools and Pie menues.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import PointerProperty
from . properties import M3SceneProperties
from . utils.registration import register_classes, unregister_classes, get_core, get_pie_menus, get_tools, get_keymaps, register_keymaps
from . icons import register_icons, unregister_icons



def register():
    global core_classes, ui_classes, op_classes, ui_keys, op_keys

    # CORE CLASSES

    core_classes = register_classes(get_core())


    # PROPERTIES

    bpy.types.Scene.M3 = PointerProperty(type=M3SceneProperties)


    # ADDITIONAL CLASSES

    op_classes = register_classes(get_tools())
    ui_classes = register_classes(get_pie_menus())


    # KEYMAPS

    # ui_keys = register_ui_keymaps()
    # op_keys = register_op_keymaps()

    keys = get_keymaps()

    register_keymaps(keys)



    register_icons()



def unregister():
    global core_lasses, ui_keys

    # CORE CLASSES

    unregister_classes(core_classes)


    # PROPERTIES

    del bpy.types.Scene.M3


    # ADDITIONAL CLASSES




    # KEYMAPS

    # for km, kmi in keymaps:
        # km.keymap_items.remove(kmi)

    # keymaps.clear()
