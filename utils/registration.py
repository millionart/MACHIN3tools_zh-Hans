import bpy
from bpy.utils import register_class, unregister_class, previews
import os
from . import MACHIN3 as m3
from .. keys import keys as keysdict


# CLASS REGISTRATION

def register_classes(classes):
    for c in classes:
        register_class(c)

    return classes


def unregister_classes(classes):
    for c in classes:
        unregister_class(c)


# KEYMAP REGISTRATION

def register_keymaps(keys):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []


    for items in keys:
        for item in items:
            keymap = item.get("keymap")
            space_type = item.get("space_type", "EMPTY")

            if keymap:
                km = kc.keymaps.new(name=keymap, space_type=space_type)

                if km:
                    idname = item.get("idname")
                    type = item.get("type")
                    value = item.get("value")

                    shift = item.get("shift", False)
                    ctrl = item.get("ctrl", False)
                    alt = item.get("alt", False)

                    kmi = km.keymap_items.new(idname, type, value, shift=shift, ctrl=ctrl, alt=alt)

                    if kmi:
                        properties = item.get("properties")

                        if properties:
                            for name, value in properties:
                                setattr(kmi.properties, name, value)

                        keymaps.append((km, kmi))
    return keymaps


def unregister_keymaps(keymaps):
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)


def get_keymaps(keys):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []

    for items in keys:
        for item in items:
            keymap = item.get("keymap")

            if keymap:
                km = kc.keymaps.get(keymap)

                if km:
                    idname = item.get("idname")

                    for kmi in km.keymap_items:
                        if kmi.idname == idname:
                            properties = item.get("properties")

                            if properties:
                                if all([getattr(kmi.properties, name, None) == value for name, value in properties]):
                                    keymaps.append((km, kmi))

                            else:
                                keymaps.append((km, kmi))

    return keymaps


# ICON REGISTRATION


def register_icons():
    path = os.path.join(m3.M3_prefs().path, "icons")
    icons = previews.new()

    for i in sorted(os.listdir(path)):
        if i.endswith(".png"):
            iconname = i[:-4]
            filepath = os.path.join(path, i)

            icons.load(iconname, filepath, 'IMAGE')

    return icons


def unregister_icons(icons):
    previews.remove(icons)


# GET CORE, TOOLS and PIES - CLASSES and KEYMAPS

def get_core():
    from .. preferences import MACHIN3toolsPreferences
    from .. properties import AppendMatsCollection, M3SceneProperties, HistoryEpochCollection, HistoryObjectsCollection, HistoryUnmirroredCollection
    from .. ui.UILists import AppendMatsUIList

    classes = []

    # PREFERENCES
    classes.extend([AppendMatsUIList, AppendMatsCollection, MACHIN3toolsPreferences])

    # PROPERTIES
    classes.extend([HistoryObjectsCollection, HistoryUnmirroredCollection, HistoryEpochCollection, M3SceneProperties])

    return classes


def get_tools():
    classes = []
    keys = []
    count = 0


    # SMART VERT
    classes, keys, count = get_smart_vert(classes, keys, count)


    # SMART EDGE

    if m3.M3_prefs().activate_smart_edge:
        from .. operators.smart_edge import SmartEdge

        classes.append(SmartEdge)
        keys.append(keysdict["SMART EDGE"])
        count +=1


    # SMART FACE

    if m3.M3_prefs().activate_smart_face:
        from .. operators.smart_face import SmartFace

        classes.append(SmartFace)
        keys.append(keysdict["SMART FACE"])
        count +=1


    # CLEAN UP

    if m3.M3_prefs().activate_clean_up:
        from .. operators.clean_up import CleanUp

        classes.append(CleanUp)
        keys.append(keysdict["CLEAN UP"])
        count +=1


    # CLIPPING TOGGLE

    if m3.M3_prefs().activate_clipping_toggle:
        from .. operators.clipping_toggle import ClippingToggle

        classes.append(ClippingToggle)
        keys.append(keysdict["CLIPPING TOGGLE"])
        count +=1


    # FOCUS

    if m3.M3_prefs().activate_focus:
        from .. operators.focus import Focus

        classes.append(Focus)
        keys.append(keysdict["FOCUS"])
        count +=1


    # MIRROR

    if m3.M3_prefs().activate_mirror:
        from .. operators.mirror import Mirror

        classes.append(Mirror)
        keys.append(keysdict["MIRROR"])
        count +=1


    # ALIGN

    if m3.M3_prefs().activate_align:
        from .. operators.align import Align

        classes.append(Align)
        keys.append(keysdict["ALIGN"])
        count +=1

    return classes, keys, count


def get_pie_menus():
    classes = []
    keymaps = []
    count = 0

    # MODES

    if m3.M3_prefs().activate_pie_modes:
        from .. ui.pies import PieModes
        from .. ui.operators.modes import EditMode, VertexMode, EdgeMode, FaceMode

        classes.append(PieModes)
        classes.extend([VertexMode, EdgeMode, FaceMode, EditMode])
        keymaps.append(keysdict["MODES PIE"])
        count += 1


    # SAVE

    if m3.M3_prefs().activate_pie_save:
        from .. ui.pies import PieSave
        from .. ui.menus import MenuAppendMaterials
        from .. ui.operators.save import New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext
        from .. ui.operators.save import AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource
        from .. ui.operators.appendmats import Add, Move, Rename, Clear, Remove

        classes.append(PieSave)
        classes.append(MenuAppendMaterials)
        classes.extend([New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext])
        classes.extend([AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource])
        classes.extend([Add, Move, Rename, Clear, Remove])
        keymaps.append(keysdict["SAVE PIE"])
        count += 1


    # SHADING

    if m3.M3_prefs().activate_pie_shading:
        from .. ui.pies import PieShading
        from .. ui.operators.shading import ShadeSolid, ShadeMaterial, ShadeRendered, ShadeWire
        from .. ui.operators.toggle_grid_wire_outline import ToggleGrid, ToggleWireframe, ToggleOutline
        from .. ui.operators.shade_smooth_flat import ShadeSmooth, ShadeFlat
        from .. ui.operators.colorize_materials import ColorizeMaterials
        from .. ui.operators.matcap_switch import MatcapSwitch

        classes.append(PieShading)
        classes.extend([ShadeSolid, ShadeMaterial, ShadeRendered, ShadeWire])
        classes.extend([ToggleGrid, ToggleWireframe, ToggleOutline])
        classes.extend([ShadeSmooth, ShadeFlat])
        classes.extend([ColorizeMaterials, MatcapSwitch])
        keymaps.append(keysdict["SHADING PIE"])
        count += 1

    # VIEWS

    if m3.M3_prefs().activate_pie_views:
        from .. ui.pies import PieViews
        from .. ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam

        classes.append(PieViews)
        classes.extend([ViewAxis, MakeCamActive, SmartViewCam])
        keymaps.append(keysdict["VIEWS PIE"])
        count += 1

    # Align
    if m3.M3_prefs().activate_pie_align:
        from .. ui.pies import PieAlign
        from .. ui.operators.align import AlignEditMesh

        classes.append(PieAlign)
        classes.append(AlignEditMesh)
        keymaps.append(keysdict["ALIGN PIE"])
        count += 1


    # WORKSPACE

    if m3.M3_prefs().activate_pie_workspace:
        from .. ui.pies import PieWorkspace
        from .. ui.operators.switch_workspace import SwitchWorkspace

        classes.append(PieWorkspace)
        classes.append(SwitchWorkspace)
        keymaps.append(keysdict["WORKSPACE PIE"])
        count += 1

    return classes, keymaps, count


# GET SPECIFIC TOOLS

def get_smart_vert(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_smart_vert:
        from .. operators.smart_vert import SmartVert

        classes.append(SmartVert)
        keys.append(keysdict["SMART VERT"])
        count +=1

    return classes, keys, count
