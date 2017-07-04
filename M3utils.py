import bpy
import os


def clear():
    import os
    os.system("clear")


def red(string):
    colored = "\033[91m" + str(string) + "\033[0m"
    return colored


def make_active(object, silent=True):
    bpy.context.scene.objects.active = object
    if not silent:
        print("Made %s active." % object.name)
    return bpy.context.scene.objects.active


def get_active():
    return bpy.context.scene.objects.active


def selected_objects():
    return bpy.context.selected_objects


def select_all(string):
    if string == "MESH":
        bpy.ops.mesh.select_all(action='SELECT')
    elif string == "OBJECT":
        bpy.ops.object.select_all(action='SELECT')


def unselect_all(string):
    if string == "MESH":
        bpy.ops.mesh.select_all(action='DESELECT')
    elif string == "OBJECT":
        bpy.ops.object.select_all(action='DESELECT')


def select(objlist):
    for obj in objlist:
        obj.select = True


def unhide_all(string="OBJECT"):
    if string == "OJBECT":
        for obj in bpy.data.objects:
            obj.hide = False
    elif string == "MESH":
        bpy.ops.mesh.reveal()


def get_mode():
    objmode = bpy.context.active_object.mode

    if objmode == "OBJECT":
        # print("object mode")
        return "OBJECT"
    elif objmode == "EDIT":
        return get_comp_mode()


def get_comp_mode():
    subobjtuple = tuple(bpy.context.scene.tool_settings.mesh_select_mode)
    if subobjtuple == (True, False, False):
        # print("edit mode: vertex")
        return "VERT"
    elif subobjtuple == (False, True, False):
        # print("edit mode: edge")
        return "EDGE"
    elif subobjtuple == (False, False, True):
        # print("edit mode: face")
        return "FACE"
    else:
        # print("Unsopported multi sub-object mode")
        return None


def set_mode(string, extend=False, expand=False):
    if string == "EDIT":
        bpy.ops.object.mode_set(mode='EDIT')
    elif string == "OBJECT":
        bpy.ops.object.mode_set(mode='OBJECT')
    elif string in ["VERT", "EDGE", "FACE"]:
        bpy.ops.mesh.select_mode(use_extend=extend, use_expand=expand, type=string)


def set_layer(layertuple):
    bpy.ops.object.move_to_layer(layers=layertuple)


def get_active_layer(string):
    if string == "INT":
        return bpy.context.scene.active_layer
    if string == "TUPLE":
        layer = bpy.context.scene.active_layer
        layertuple = ()
        for i in range(20):
            if i == layer:
                layertuple += (True,)
            else:
                layertuple += (False,)
        return layertuple


def show_all_layers():
    for i in range(20):
        bpy.context.scene.layers[i] = True


def show_only_layer(layerint):
    for i in range(20):
        if i == layerint:
            bpy.context.scene.layers[i] = True
        else:
            bpy.context.scene.layers[i] = False


def change_context(string):
    area = bpy.context.area
    old_type = area.type
    area.type = string
    return old_type


def change_pivot(string):
    space_data = bpy.context.space_data
    old_type = space_data.pivot_point
    space_data.pivot_point = string
    return old_type


def set_timestamp(object, timestamp=None, silent=True):
    if timestamp is None:
        import time
        timestamp = time.time()
    object["timestamp"] = timestamp
    if not silent:
        print("Set '%s' timestamp to '%f'." % (object.name, timestamp))
    return timestamp


def get_timestamp(object):
    try:
        timestamp = object["timestamp"]
    except:
        timestamp = None
    return timestamp


def get_AM_library_path():
    addons = bpy.context.user_preferences.addons

    for addonname in addons.keys():
        if "asset_management" in addonname:
            return addons[addonname].preferences.asset_M_library_path


def HOps_check():
    return addon_check("HOps")


def AM_check():
    return addon_check("asset_management", precise=False)


def addon_check(string, precise=True):
    for addon in bpy.context.user_preferences.addons.keys():
        if precise:
            if string == addon:
                return True
        else:
            if string.lower() in addon.lower():
                return True
    return False


def move_to_cursor(obj, scene):
    obj.select = True
    make_active(obj)
    obj.location = bpy.context.scene.cursor_location


def lock(obj, location=True, rotation=True, scale=True):
    if location:
        for idx, _ in enumerate(obj.lock_location):
            obj.lock_location[idx] = True

    if rotation:
        for idx, _ in enumerate(obj.lock_rotation):
            obj.lock_rotation[idx] = True

    if scale:
        for idx, _ in enumerate(obj.lock_scale):
            obj.lock_scale[idx] = True


def open_folder(pathstring):
    import platform
    import subprocess

    if platform.system() == "Windows":
        os.startfile(pathstring)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", pathstring])
    else:
        # subprocess.Popen(["xdg-open", pathstring])
        os.system('xdg-open "%s" %s &' % (pathstring, "> /dev/null 2> /dev/null"))  # > sends stdout,  2> sends stderr


def addon_prefs(addonstring):
    return bpy.context.user_preferences.addons[addonstring].preferences


def DM_prefs():
    return bpy.context.user_preferences.addons["DECALmachine"].preferences


def M3_prefs():
    return bpy.context.user_preferences.addons["MACHIN3tools"].preferences


def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)
