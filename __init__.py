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
    "version": (0, 2),
    "blender": (2, 78, 0),
    "location": "",
    "description": "A collection of blender python scripts.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import BoolProperty
from . import developer_utils as du
from . import M3utils as m3

modules = du.setup_addon_modules(__path__, __name__, "bpy" in locals())


# TODO: add automatic custom blender keymaps option
# TODO: OSD feedback, so you dont have to check into the op props to verify a tool did what you want it to do


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)

    pieobjecteditmodehide = BoolProperty(name="Auto Hide", default=False)
    pieobjecteditmodeshow = BoolProperty(name="Auto Reveal", default=False)


class MACHIN3Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    M3path = __path__[0]

    activate_pies = BoolProperty(name="Pie Menus", default=False)

    activate_ShadingSwitch = BoolProperty(name="Shading Switch", default=False)
    activate_RedMode = BoolProperty(name="Red Mode", default=False)
    activate_CenterCube = BoolProperty(name="Center Cube", default=False)
    activate_CleansUpGood = BoolProperty(name="Cleans Up Good", default=False)
    activate_ClippingToggle = BoolProperty(name="Clipping Plane Toggle", default=False)
    activate_Focus = BoolProperty(name="Focus", default=False)
    # activate_ThemeSwitch = BoolProperty(name="Theme Switch", default=False)
    activate_Mirror = BoolProperty(name="Mirror", default=False)
    activate_StarConnect = BoolProperty(name="Star Connect", default=False)
    activate_SmartModes = BoolProperty(name="Smart Modes", default=False)
    activate_CleanoutMaterials = BoolProperty(name="Cleanout Materials", default=False)
    activate_CleanoutUVs = BoolProperty(name="Cleanout UVs", default=False)
    activate_CleanoutTransforms = BoolProperty(name="Cleanout Transforms", default=False)
    activate_SlideExtend = BoolProperty(name="Slide Extend", default=False)
    activate_LockItAll = BoolProperty(name="Lock It All", default=False)
    activate_HideMeshes = BoolProperty(name="Hide Meshes", default=False)
    activate_ModMachine = BoolProperty(name="Mod Machine", default=False)
    activate_CameraHelper = BoolProperty(name="Camera Helper", default=False)
    activate_ChildOf = BoolProperty(name="Child Of", default=False)
    activate_FlipNormals = BoolProperty(name="Flip Normals", default=False)

    def draw(self, context):
        layout=self.layout

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        col = layout.column()

        col.label("Activating modules requires saving user preferences and re-starting Blender.")
        col.separator()

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pies", toggle=True)
        row.label(" Pies based on Wazou's Pie Menus")

        # SHADING SWITCH

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ShadingSwitch", toggle=True)
        row.label("Switches between Material and Solid shading modes. Also re-assigns Z key for wireframe switching and Shift + Z for render switching accordingly.")
        du.show_keymap(self.activate_ShadingSwitch, kc, "3D View", "machin3.shading_switch", col)

        # RED MODE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_RedMode", toggle=True)
        row.label("In SOLID mode: switch to red matcap and back. In MATERIAL mode: switch turn bevels of WStep materials red and.")
        du.show_keymap(self.activate_RedMode, kc, "3D View", "machin3.red_mode", col)

        # Center Cube

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CenterCube", toggle=True)
        row.label("If nothing is selected, places a cube at the cursor location, with any of X/Y/Z zeroed out, enters edit mode, selects all and initiates the scale tool. If objects are selected, it zeroes out any of X/Y/Z.")
        du.show_keymap(self.activate_CenterCube, kc, "Object Mode", "machin3.center_cube", col)

        # Cleans Up Good

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleansUpGood", toggle=True)
        row.label("Removes doubles, dissolves degenerates, deletes loose vertices and edges, recalculates normals, dissolves 2-edged vertices, selects non-manifold geometry. Works in edit mode and object mode(incl. on multiple objects).")
        du.show_keymap(self.activate_CleansUpGood, kc, "Mesh", "machin3.clean_up", col)

        # CLIPPING TOGGLE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ClippingToggle", toggle=True)
        row.label("Toggle through different clipping plane settings")
        du.show_keymap(self.activate_ClippingToggle, kc, "3D View", "machin3.clipping_toggle", col)

        # FOCUS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Focus", toggle=True)
        row.label("Disables all Mirror modifiers of the selected objects, then enters local view. Renables mirror modifers again, when exiting localview.")
        du.show_keymap(self.activate_Focus, kc, "Object Mode", "machin3.focus", col)

        # MIRROR

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Mirror", toggle=True)
        row.label("Mirrors selected objects across the active object, allows mirroring of multiple objects at once and supports DECALmachine.")
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_x", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_y", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_z", col)

        # STAR CONNECT

        row = col.split(percentage=0.2)
        row.prop(self, "activate_StarConnect", toggle=True)
        row.label("In Vert mode, connects all selected verts to the last one of the selection, in Face mode it creates a center star vert")
        du.show_keymap(self.activate_StarConnect, kc, "Mesh", "machin3.star_connect", col)

        # SMART MODES

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SmartModes", toggle=True)
        row.label("In Vert mode connects vert path, in edge mode is turns the edge, in face mode it converts the selection to a bounder loop.")
        du.show_keymap(self.activate_SmartModes, kc, "Mesh", "machin3.smart_modes", col)

        # CLEANOUT MATERIALS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutMaterials", toggle=True)
        row.label("Removes all material assignments and all materials from the scene.")

        # CLEANOUT UVS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutUVs", toggle=True)
        row.label("Removes all UV channels from selected objects.")

        # CLEANOUT TRANSFORM ORIENTATIONS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutTransforms", toggle=True)
        row.label("Removes all custom transform orientations.")

        # SLIDE EXTEND

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SlideExtend", toggle=True)
        row.label("Moves selected vert away or closer to active vert.")
        du.show_keymap(self.activate_SlideExtend, kc, "Mesh", "machin3.slide_extend", col)

        # LOCK IT ALL

        row = col.split(percentage=0.2)
        row.prop(self, "activate_LockItAll", toggle=True)
        row.label("Locks any or all selected objects' transforms")

        # HIDE MESHES

        row = col.split(percentage=0.2)
        row.prop(self, "activate_HideMeshes", toggle=True)
        row.label("Hides Meshes of selection in Object Mode.")
        du.show_keymap(self.activate_HideMeshes, kc, "Object Mode", "machin3.hide_meshes", col)

        # MOD MACHINE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ModMachine", toggle=True)
        row.label("Applys/Shows/Hides the entire modifier stack or any of the selceted mods on objects in selection.")

        # CAMERA HELPER

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CameraHelper", toggle=True)
        row.label("Creates a new camera from view if nothing is selected. If Camera is selcted, aligns camera to current view and makes it the scene camera.")
        du.show_keymap(self.activate_CameraHelper, kc, "Object Mode", "machin3.camera_helper", col)

        # CHILD OF

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ChildOf", toggle=True)
        row.label("Child of's instead of parents. Works on geo and bones. On geo, can be fired multile times to switch between 'set inverse' and 'clear inverse. On geo defaults to 'set inverse', while on bones defaults to 'clear inverse'.")

        # FLIP NORMALS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_FlipNormals", toggle=True)
        row.label("Flips normals of selected objects.")


class VIEW3D_MT_object_machin3tools(bpy.types.Menu):
    bl_label = "MACHIN3tools"

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_CenterCube:
            column.operator("machin3.center_cube", text="Center Cube")
        if m3.M3_prefs().activate_CleanoutMaterials:
            column.operator("machin3.cleanout_materials", text="Cleanout Materials")
        if m3.M3_prefs().activate_CleanoutUVs:
            column.operator("machin3.cleanout_uvs", text="Cleanout UVs")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_LockItAll:
            column.operator("machin3.lock_it_all", text="Lock It All")
        if m3.M3_prefs().activate_HideMeshes:
            column.operator("machin3.hide_meshes", text="Hide Meshes")
        if m3.M3_prefs().activate_ModMachine:
            column.operator("machin3.mod_machine", text="Mod Machine")
        if m3.M3_prefs().activate_CameraHelper:
            column.operator("machin3.camera_helper", text="Camera Helper")
        if m3.M3_prefs().activate_ChildOf:
            column.operator("machin3.child_of", text="Child Of")
        if m3.M3_prefs().activate_FlipNormals:
            column.operator("machin3.flip_normals", text="Flip Normals")


class VIEW3D_MT_edit_mesh_machin3tools(bpy.types.Menu):
    bl_label = "MACHIN3tools"

    # TODO: comp mode availability check

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_SmartModes:
            column.operator("machin3.smart_modes", text="Smart Modes")
        if m3.M3_prefs().activate_StarConnect:
            column.operator("machin3.star_connect", text="Star Connect")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_SlideExtend:
            column.operator("machin3.slide_extend", text="Slide Extend")


def edit_menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_machin3tools")
    self.layout.separator()


def object_menu_func(self, context):
    self.layout.menu("VIEW3D_MT_object_machin3tools")
    self.layout.separator()


def register_MACHIN3_keys(wm, keymaps):
    # SHADING SWITCH

    if m3.M3_prefs().activate_ShadingSwitch:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.shading_switch", 'BUTTON5MOUSE', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # RED MODE

    if m3.M3_prefs().activate_RedMode:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.red_mode", 'BUTTON5MOUSE', 'PRESS', alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # CENTER CUBE

    if m3.M3_prefs().activate_CenterCube:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.center_cube", 'C', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # CLEANS UP GOOD

    if m3.M3_prefs().activate_CleansUpGood:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.clean_up", "THREE", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # CLIPPING PLANE TOGGLE

    if m3.M3_prefs().activate_ClippingToggle:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.clipping_toggle", "BUTTON5MOUSE", "PRESS")

    # FOCUS

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.focus", "F", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # THEME SWITCH

    # if m3.M3_prefs().activate_ThemeSwitch:
        # km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        # kmi = km.keymap_items.new("machin3.theme_switch", "BUTTON5MOUSE", "PRESS", ctrl=True)

    # MIRROR

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror_x", "X", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_y", "Y", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_z", "Z", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # STAR MODES

    if m3.M3_prefs().activate_StarConnect:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.star_connect", "TWO", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # SMART MODES

    if m3.M3_prefs().activate_SmartModes:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_modes", "TWO", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # SLIDE EXTEND

    if m3.M3_prefs().activate_SlideExtend:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.slide_extend", "E", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # HIDE MESHES

    if m3.M3_prefs().activate_HideMeshes:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.hide_meshes", "H", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # CAMERA HELPER

    if m3.M3_prefs().activate_CameraHelper:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.camera_helper", "NUMPAD_0", "PRESS", alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # CHILD OF

    if m3.M3_prefs().activate_ChildOf:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.child_of", "P", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))


def register_pie_keys(wm, keymaps):
    # SELECT MODE

    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
    kmi.properties.name = "pie.objecteditmode"
    kmi.active = True
    keymaps.append((km, kmi))

    # LAYOUTS

    km = wm.keyconfigs.addon.keymaps.new(name='Screen')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', ctrl=True)
    kmi.properties.name = "pie.areaviews"
    kmi.active = True
    keymaps.append((km, kmi))

    # SNAPPING

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'MIDDLEMOUSE', 'PRESS', alt=True)
    kmi.properties.name = "pie.snapping"
    kmi.active = True
    keymaps.append((km, kmi))

    # ORIENTATIONS

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', alt=True)
    kmi.properties.name = "pie.orientation"
    kmi.active = True
    keymaps.append((km, kmi))

    # OBJECT SHADING

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', alt=True)
    kmi.properties.name = "pie.objectshading"
    kmi.active = True
    keymaps.append((km, kmi))

    # ALIGN

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', alt=True)
    kmi.properties.name = "pie.align"
    kmi.active = True
    keymaps.append((km, kmi))

    # SAVE, OPEN, APPEND, LINK, ...

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True)
    kmi.properties.name = "pie.saveopen"
    kmi.active = True
    keymaps.append((km, kmi))

    # UV SELECT MODE

    km = wm.keyconfigs.addon.keymaps.new(name='Image', space_type='IMAGE_EDITOR')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
    kmi.properties.name = "pie.uvsselectmode"
    kmi.active = True
    keymaps.append((km, kmi))

    # UV WELD, ALIGN

    km = wm.keyconfigs.addon.keymaps.new(name='UV Editor')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
    kmi.properties.name = "pie.uvsweldalign"
    kmi.active = True
    keymaps.append((km, kmi))


MACHIN3_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.machin3 = bpy.props.PointerProperty(type=MACHIN3Settings)

    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(edit_menu_func)
    bpy.types.VIEW3D_MT_object_specials.prepend(object_menu_func)

    wm = bpy.context.window_manager

    # MACHIN3 addon KEYMAPS

    register_MACHIN3_keys(wm, MACHIN3_keymaps)

    # PIE KEYMAPS

    if m3.M3_prefs().activate_pies:
        register_pie_keys(wm, MACHIN3_keymaps)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(edit_menu_func)
    bpy.types.VIEW3D_MT_object_specials.remove(object_menu_func)

    for km, kmi in MACHIN3_keymaps:
        km.keymap_items.remove(kmi)

    MACHIN3_keymaps.clear()
