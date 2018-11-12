import bpy


def register_keymaps():
    keys = []

    keys = register_ui_keymaps(keys)
    keys = register_op_keymaps(keys)

    return keys


def register_ui_keymaps(keys):
    wm = bpy.context.window_manager

    # SELECT MODE

    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_select_modes"
    kmi.active = True
    keys.append((km, kmi))


    # CHANGE SHADING

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_UP', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_change_shading"
    kmi.active = True
    keys.append((km, kmi))


    # VIEWS and CAMS

    km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAGE_DOWN', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_views_and_cams"
    kmi.active = True
    keys.append((km, kmi))


    # SAVE, OPEN, APPEND

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True)
    kmi.properties.name = "VIEW3D_MT_MACHIN3_save_open_append"
    kmi.active = True
    keys.append((km, kmi))


    # SWITCH WORKSPACE

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAUSE', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_switch_workspace"
    kmi.active = True
    keys.append((km, kmi))

    return keys


def register_op_keymaps(keys):
    wm = bpy.context.window_manager

    # SMART VERT

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS")
    kmi.properties.type = "LAST"
    keys.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS", shift=True)
    kmi.properties.type = "CENTER"
    keys.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("machin3.smart_vert", "ONE", "PRESS", alt=True)
    kmi.properties.type = "SMART"
    keys.append((km, kmi))


    # SMART EDGE

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("machin3.smart_edge", "TWO", "PRESS")
    keys.append((km, kmi))


    # SMART FACE

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new("machin3.smart_face", "FOUR", "PRESS")
    keys.append((km, kmi))

    return keys
