import bpy
from . utils import MACHIN3 as m3


def register_op_keymaps():
    keys = []

    wm = bpy.context.window_manager

    # SMART VERT

    if m3.M3_prefs().activate_smart_vert:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS")
        kmi.properties.type = "LAST"
        kmi.properties.slide_override = False
        keys.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS", shift=True)
        kmi.properties.type = "CENTER"
        kmi.properties.slide_override = False
        keys.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS", alt=True)
        kmi.properties.type = "SMART"
        kmi.properties.slide_override = False
        keys.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS", shift=True, alt=True)
        kmi.properties.slide_override = True
        keys.append((km, kmi))


    # SMART EDGE

    if m3.M3_prefs().activate_smart_vert:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_edge", "TWO", "PRESS")
        keys.append((km, kmi))


    # SMART FACE

    if m3.M3_prefs().activate_smart_vert:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_face", "FOUR", "PRESS")
        keys.append((km, kmi))


    # CLEAN UP

    if m3.M3_prefs().activate_clean_up:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.clean_up", "THREE", "PRESS")
        keys.append((km, kmi))

    # CLIPPING TOGGLE

    if m3.M3_prefs().activate_clipping_toggle:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.clipping_toggle", "BUTTON5MOUSE", "PRESS")
        keys.append((km, kmi))


    # FOCUS

    if m3.M3_prefs().activate_focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.focus", "F", "PRESS", ctrl=True)
        keys.append((km, kmi))


    # MIRROR

    if m3.M3_prefs().activate_mirror:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror", "X", "PRESS", alt=True, shift=True)
        kmi.properties.use_x = True
        kmi.properties.use_y = False
        kmi.properties.use_z = False
        keys.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror", "Y", "PRESS", alt=True, shift=True)
        kmi.properties.use_x = False
        kmi.properties.use_y = True
        kmi.properties.use_z = False
        keys.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror", "Z", "PRESS", alt=True, shift=True)
        kmi.properties.use_x = False
        kmi.properties.use_y = False
        kmi.properties.use_z = True
        keys.append((km, kmi))


    # ALIGN

    if m3.M3_prefs().activate_align:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.align", "A", "PRESS", alt=True)
        keys.append((km, kmi))

    return keys


def register_ui_keymaps():
    keys = []

    wm = bpy.context.window_manager

    # MODES

    if m3.M3_prefs().activate_pie_modes:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_MACHIN3_modes"
        keys.append((km, kmi))


    # SAVE

    if m3.M3_prefs().activate_pie_save:
        km = wm.keyconfigs.addon.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True)
        kmi.properties.name = "VIEW3D_MT_MACHIN3_save"
        keys.append((km, kmi))


    # SHADING

    if m3.M3_prefs().activate_pie_shading:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_UP', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_MACHIN3_shading"
        keys.append((km, kmi))


    # VIEWS

    if m3.M3_prefs().activate_pie_views:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_DOWN', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_MACHIN3_views"
        keys.append((km, kmi))


    # WORKSPACE

    if m3.M3_prefs().activate_pie_workspace:
        km = wm.keyconfigs.addon.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'PAUSE', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_MACHIN3_workspace"
        keys.append((km, kmi))

    return keys
