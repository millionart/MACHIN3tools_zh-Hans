import bpy
from bpy.utils import register_class, unregister_class, previews
import os
from . import MACHIN3 as m3
from .. keys import keys as keysdict
from .. classes import classes as classesdict


# CLASS REGISTRATION

def register_classes(classlists, debug=False):
    classes = []

    for classlist in classlists:
        for fr, imps in classlist:
            impline = "from ..%s import %s" % (fr, ", ".join([i[0] for i in imps]))
            classline = "classes.extend([%s])" % (", ".join([i[0] for i in imps]))

            exec(impline)
            exec(classline)

    for c in classes:
        if debug:
            print("REGISTERING", c)

        register_class(c)

    return classes


def unregister_classes(classes, debug=False):
    for c in classes:
        if debug:
            print("UN-REGISTERING", c)

        unregister_class(c)


def get_classes(classlist):
    classes = []

    for fr, imps in classlist:
        if "operators" in fr:
            type = "OT"
        elif "pies" in fr or "menus" in fr:
            type = "MT"

        for imp in imps:
            idname = imp[1]
            rna_name = "MACHIN3_%s_%s" % (type, idname)

            c = getattr(bpy.types, rna_name, False)

            if c:
                classes.append(c)

    return classes


# KEYMAP REGISTRATION

def register_keymaps(keylists):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []


    for keylist in keylists:
        for item in keylist:
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


def get_keymaps(keylist):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []

    for item in keylist:
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


# RUNTIME TOOL (DE)ACTIVATION

def activate(self, register, tool):
    debug=True
    debug=False

    name = tool.replace("_", " ").title()

    # REGISTER

    if register:
        classlist, keylist, _ = eval("get_%s()" % (tool))

        # CLASSES

        # register tool/pie class
        classes = register_classes(classlist, debug=debug)


        # update classes registered in __init__.py at startup, necessary for addon unregistering
        from .. import classes as startup_classes

        for c in classes:
            if c not in startup_classes:
                startup_classes.append(c)

        # KEYMAPS

        # register tool keymaps
        keymaps = register_keymaps(keylist)

        # update keymaps registered in __init__.py at startup, necessary for addon unregistering
        from .. import keymaps as startup_keymaps
        for k in keymaps:
            if k not in startup_keymaps:
                startup_keymaps.append(k)

        if classes:
            print("Registered MACHIN3tools' %s" % (name))

        classlist.clear()
        keylist.clear()


    # UN-REGISTER

    else:
        # KEYMAPS

        keylist = keysdict[tool.upper()]
        keymaps = get_keymaps(keylist)

        # update keymaps registered in __init__.py at startup, necessary for addon unregistering
        from .. import keymaps as startup_keymaps
        for k in keymaps:
            if k in startup_keymaps:
                startup_keymaps.remove(k)

        # unregister tool keymaps
        unregister_keymaps(keymaps)


        # CLASSES

        classlist = classesdict[tool.upper()]


        classes = get_classes(classlist)

        # update classes registered in __init__.py at startup, necessary for addon unregistering
        from .. import classes as startup_classes

        for c in classes:
            if c in startup_classes:
                startup_classes.remove(c)

        # unregister tool classes

        unregister_classes(classes, debug=debug)

        if classes:
            print("Unregistered MACHIN3tools' %s" % (name))


# GET CORE, TOOLS and PIES - CLASSES and KEYMAPS - for startup registration

def get_core():
    return [classesdict["CORE"]]


def get_tools():
    classlists = []
    keylists = []
    count = 0


    # SMART VERT
    classlists, keylists, count = get_smart_vert(classlists, keylists, count)


    # SMART EDGE
    classlists, keylists, count = get_smart_edge(classlists, keylists, count)


    # SMART FACE
    classlists, keylists, count = get_smart_face(classlists, keylists, count)


    # CLEAN UP
    classlists, keylists, count = get_clean_up(classlists, keylists, count)


    # CLIPPING TOGGLE
    classlists, keylists, count = get_clipping_toggle(classlists, keylists, count)


    # FOCUS
    classlists, keylists, count = get_focus(classlists, keylists, count)


    # MIRROR
    classlists, keylists, count = get_mirror(classlists, keylists, count)


    # ALIGN
    classlists, keylists, count = get_align(classlists, keylists, count)

    return classlists, keylists, count


def get_pie_menus():
    classlists = []
    keylists = []
    count = 0

    # MODES

    classlists, keylists, count = get_modes_pie(classlists, keylists, count)


    # SAVE

    classlists, keylists, count = get_save_pie(classlists, keylists, count)


    # SHADING

    classlists, keylists, count = get_shading_pie(classlists, keylists, count)


    # VIEWS

    classlists, keylists, count = get_views_pie(classlists, keylists, count)


    # ALIGN

    classlists, keylists, count = get_align_pie(classlists, keylists, count)


    # WORKSPACE

    classlists, keylists, count = get_workspace_pie(classlists, keylists, count)

    return classlists, keylists, count


# GET SPECIFIC TOOLS

def get_smart_vert(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_smart_vert:
        from .. operators.smart_vert import SmartVert

        classlists.append(classesdict["SMART_VERT"])
        keylists.append(keysdict["SMART_VERT"])
        count +=1

    return classlists, keylists, count


def get_smart_edge(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_smart_edge:
        from .. operators.smart_edge import SmartEdge

        classlists.append(classesdict["SMART_EDGE"])
        keylists.append(keysdict["SMART_EDGE"])
        count +=1

    return classlists, keylists, count


def get_smart_face(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_smart_face:
        classlists.append(classesdict["SMART_FACE"])
        keylists.append(keysdict["SMART_FACE"])
        count +=1

    return classlists, keylists, count


def get_clean_up(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_clean_up:
        classlists.append(classesdict["CLEAN_UP"])
        keylists.append(keysdict["CLEAN_UP"])
        count +=1

    return classlists, keylists, count


def get_clipping_toggle(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_clipping_toggle:
        classlists.append(classesdict["CLIPPING_TOGGLE"])
        keylists.append(keysdict["CLIPPING_TOGGLE"])
        count +=1

    return classlists, keylists, count


def get_focus(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_focus:
        classlists.append(classesdict["FOCUS"])
        keylists.append(keysdict["FOCUS"])
        count +=1

    return classlists, keylists, count


def get_mirror(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_mirror:
        classlists.append(classesdict["MIRROR"])
        keylists.append(keysdict["MIRROR"])
        count +=1

    return classlists, keylists, count


def get_align(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_align:
        classlists.append(classesdict["ALIGN"])
        keylists.append(keysdict["ALIGN"])
        count +=1

    return classlists, keylists, count


# GET SPECIFIC PIES

def get_modes_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_modes_pie:
        classlists.append(classesdict["MODES_PIE"])
        keylists.append(keysdict["MODES_PIE"])
        count += 1

    return classlists, keylists, count


def get_save_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_save_pie:
        classlists.append(classesdict["SAVE_PIE"])
        keylists.append(keysdict["SAVE_PIE"])
        count += 1

    return classlists, keylists, count


def get_shading_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_shading_pie:
        classlists.append(classesdict["SHADING_PIE"])
        keylists.append(keysdict["SHADING_PIE"])
        count += 1

    return classlists, keylists, count


def get_views_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_views_pie:
        # from .. ui.pies import PieViews
        # from .. ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam

        # classes.append(PieViews)
        # classes.extend([ViewAxis, MakeCamActive, SmartViewCam])

        classlists.append(classesdict["VIEWS_PIE"])
        keylists.append(keysdict["VIEWS_PIE"])
        count += 1

    return classlists, keylists, count


def get_align_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_align_pie:
        classlists.append(classesdict["ALIGN_PIE"])
        keylists.append(keysdict["ALIGN_PIE"])
        count += 1

    return classlists, keylists, count


def get_workspace_pie(classlists=[], keylists=[], count=0):
    if m3.M3_prefs().activate_workspace_pie:
        classlists.append(classesdict["WORKSPACE_PIE"])
        keylists.append(keysdict["WORKSPACE_PIE"])
        count += 1

    return classlists, keylists, count
