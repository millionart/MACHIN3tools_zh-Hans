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

    for tool in keys:
        for item in tool:
            keymap = tool.get("keymap")

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


# RUNTIME TOOL (DE)ACTIVATION

def activate_tool(self, rna_name, register, tool):
    c = getattr(bpy.types, rna_name, False)

    if c:
        # UNREGISTER

        # NOTE: unregistering pies or muli class pies, is incomplete, because we cant just import the classes to unregister them
        # ####: attmepting to do this via the get_some_pie() function resuls in an empty class list, because the classes are importd already
        # ####: to unrgister them you need to pick them from bpy.types as you do with the c class
        # ####: unfortunately it can be quite a lot of classes and I don't want to pass all their rna names in as strings, hmm
        # ####: since unregistering is incomplete, re-registering will throw an excpetion.
        # ####: it could be done by mirroring the keymap approach, where all the rna names are loaded in from a json

        if not register:

            # KEYMAPS

            keys = [keysdict[tool.upper()]]
            keymaps = get_keymaps(keys)

            # update keymaps registered in __init__.py at startup, necessary for addon unregistering
            from .. import keymaps as startup_keymaps
            for k in keymaps:
                if k in startup_keymaps:
                    startup_keymaps.remove(k)

            # unregister tool keymaps
            unregister_keymaps(keymaps)


            # CLASSES

            # update classes registered in __init__.py at startup, necessary for addon unregistering
            from .. import classes as startup_classes
            if c in startup_classes:
                startup_classes.remove(c)

            # unregister tool class
            unregister_classes([c])
            print("Unregistered %s" % (c.bl_idname))

    else:
        # REGISTER

        if register:
            classes, keys, _ = eval("get_%s()" % (tool))

            # CLASSES

            # register tool class
            register_classes(classes)

            # update classes registered in __init__.py at startup, necessary for addon unregistering
            from .. import classes as startup_classes
            if c not in startup_classes:
                startup_classes.extend(classes)


            # KEYMAPS

            # register tool keymaps
            keymaps = register_keymaps(keys)

            # update keymaps registered in __init__.py at startup, necessary for addon unregistering
            from .. import keymaps as startup_keymaps
            for k in keymaps:
                if k not in startup_keymaps:
                    startup_keymaps.append(k)


            print("Registered %s" % (classes[0].bl_idname))
            classes.clear()
            keys.clear()


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
    classes, keys, count = get_smart_edge(classes, keys, count)


    # SMART FACE
    classes, keys, count = get_smart_face(classes, keys, count)


    # CLEAN UP
    classes, keys, count = get_clean_up(classes, keys, count)


    # CLIPPING TOGGLE
    classes, keys, count = get_clipping_toggle(classes, keys, count)


    # FOCUS
    classes, keys, count = get_focus(classes, keys, count)


    # MIRROR
    classes, keys, count = get_mirror(classes, keys, count)


    # ALIGN
    classes, keys, count = get_align(classes, keys, count)

    return classes, keys, count


def get_pie_menus():
    classes = []
    keys = []
    count = 0

    # MODES

    classes, keys, count = get_modes_pie(classes, keys, count)


    # SAVE

    if m3.M3_prefs().activate_save_pie:
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
        keys.append(keysdict["SAVE_PIE"])
        count += 1


    # SHADING

    if m3.M3_prefs().activate_shading_pie:
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
        keys.append(keysdict["SHADING_PIE"])
        count += 1

    # VIEWS

    if m3.M3_prefs().activate_views_pie:
        from .. ui.pies import PieViews
        from .. ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam

        classes.append(PieViews)
        classes.extend([ViewAxis, MakeCamActive, SmartViewCam])
        keys.append(keysdict["VIEWS_PIE"])
        count += 1

    # Align
    if m3.M3_prefs().activate_align_pie:
        from .. ui.pies import PieAlign
        from .. ui.operators.align import AlignEditMesh

        classes.append(PieAlign)
        classes.append(AlignEditMesh)
        keys.append(keysdict["ALIGN_PIE"])
        count += 1


    # WORKSPACE

    if m3.M3_prefs().activate_workspace_pie:
        from .. ui.pies import PieWorkspace
        from .. ui.operators.switch_workspace import SwitchWorkspace

        classes.append(PieWorkspace)
        classes.append(SwitchWorkspace)
        keys.append(keysdict["WORKSPACE_PIE"])
        count += 1

    return classes, keys, count


# GET SPECIFIC TOOLS

def get_smart_vert(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_smart_vert:
        from .. operators.smart_vert import SmartVert

        classes.append(SmartVert)
        keys.append(keysdict["SMART_VERT"])
        count +=1

    return classes, keys, count


def get_smart_edge(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_smart_edge:
        from .. operators.smart_edge import SmartEdge

        classes.append(SmartEdge)
        keys.append(keysdict["SMART_EDGE"])
        count +=1

    return classes, keys, count


def get_smart_face(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_smart_face:
        from .. operators.smart_face import SmartFace

        classes.append(SmartFace)
        keys.append(keysdict["SMART_FACE"])
        count +=1

    return classes, keys, count


def get_clean_up(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_clean_up:
        from .. operators.clean_up import CleanUp

        classes.append(CleanUp)
        keys.append(keysdict["CLEAN_UP"])
        count +=1

    return classes, keys, count


def get_clipping_toggle(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_clipping_toggle:
        from .. operators.clipping_toggle import ClippingToggle

        classes.append(ClippingToggle)
        keys.append(keysdict["CLIPPING_TOGGLE"])
        count +=1

    return classes, keys, count


def get_focus(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_focus:
        from .. operators.focus import Focus

        classes.append(Focus)
        keys.append(keysdict["FOCUS"])
        count +=1

    return classes, keys, count


def get_mirror(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_mirror:
        from .. operators.mirror import Mirror

        classes.append(Mirror)
        keys.append(keysdict["MIRROR"])
        count +=1

    return classes, keys, count


def get_align(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_align:
        from .. operators.align import Align

        classes.append(Align)
        keys.append(keysdict["ALIGN"])
        count +=1

    return classes, keys, count


# GET SPECIFIC PIES

def get_modes_pie(classes=[], keys=[], count=0):
    if m3.M3_prefs().activate_modes_pie:
        from .. ui.pies import PieModes
        from .. ui.operators.modes import EditMode, VertexMode, EdgeMode, FaceMode

        classes.append(PieModes)
        classes.extend([VertexMode, EdgeMode, FaceMode, EditMode])
        keys.append(keysdict["MODES_PIE"])
        count += 1

    return classes, keys, count
