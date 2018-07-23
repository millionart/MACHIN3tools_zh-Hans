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


    # Switch Workspace

    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'PAUSE', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_MACHIN3_switch_workspace"
    kmi.active = True
    keys.append((km, kmi))

    return keys


def register_op_keymaps(keys):
    return keys
