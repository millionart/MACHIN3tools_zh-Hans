import bpy
import os
import shutil
from .. utils import MACHIN3 as m3


# TODO: do the prefs part based on a dictionary?


class Customize(bpy.types.Operator):
    bl_idname = "machin3.customize"
    bl_label = "MACHIN3: Customize"
    bl_description = "Customize various Blender preferences, settings and keymaps."
    bl_options = {'REGISTER'}


    def execute(self, context):
        scriptspath = bpy.utils.user_resource('SCRIPTS')
        datafilespath = bpy.utils.user_resource('DATAFILES')

        resourcespath = os.path.join(m3.M3_prefs().path, "resources")

        # WINDOW (is read only)
        # bpy.context.window.screen.areas[0].regions[0].alignment = "TOP"
        # bpy.context.area.region[0].alignment = "TOP"

        # SET CURSOR TOOL
        if context.area.type == "VIEW_3D":
            bpy.ops.wm.tool_set_by_name(name="Cursor")

        # THEME
        if m3.M3_prefs().custom_theme:
            self.theme(scriptspath, resourcespath)

        # MATCAPS + DEFAULT SHADING
        if m3.M3_prefs().custom_matcaps:
            self.matcaps(context, resourcespath, datafilespath)

        # OVERLAYS
        if m3.M3_prefs().custom_overlays:
            self.overlays(context)

        # PREFERENCES
        self.preferences(context)


        # CUSTOM KEYMAPS
        if m3.M3_prefs().custom_keymaps:
            self.keymaps(context)


        # START UP
        # copy and load start up file, which includes workspaces
        # """

        return {'FINISHED'}

    def keymaps(self, context):
        def modify_keymaps(kc):
            # WINDOW
            km = kc.keymaps.get("Window")
            for kmi in km.keymap_items:
                if kmi.idname == "wm.open_mainfile":
                    kmi.active = False

                if kmi.idname == "wm.doc_view_manual_ui_context":
                    kmi.active = False


            # SCREEN

            km = kc.keymaps.get("Screen")
            for kmi in km.keymap_items:
                if kmi.idname == "ed.undo":
                    kmi.type = "F1"
                    kmi.ctrl = False

                if kmi.idname == "ed.redo":
                    kmi.type = "F2"
                    kmi.ctrl = False
                    kmi.shift = False

                if kmi.idname == "ed.undo_history":
                    kmi.type = "F1"
                    kmi.ctrl = False
                    kmi.alt = True

                if kmi.idname == "screen.redo_last":
                    kmi.type = "BUTTON4MOUSE"

                if kmi.idname == "screen.screen_full_area":
                    if kmi.properties.use_hide_panels:
                        kmi.shift = True
                        kmi.alt = False
                        kmi.ctrl = False

                    else:
                        kmi.active = False


            # 3D VIEW

            km = kc.keymaps.get("3D View")
            for kmi in km.keymap_items:
                if kmi.idname == "view3d.view_selected":
                    if kmi.type == "NUMPAD_PERIOD" and not kmi.properties.use_all_regions:
                        kmi.type = "F"

                if kmi.idname == "view3d.cursor3d":
                    kmi.type = "RIGHTMOUSE"
                    kmi.alt = True
                    kmi.shift = False

                if kmi.idname == "view3d.select":
                    if kmi.value == "CLICK":
                        if not any([getattr(kmi.properties, name, False) for name in ["extend", "deselect", "toggle", "center", "enumerate", "object"]]):
                            kmi.value = "PRESS"

                        elif kmi.properties.toggle and not any([getattr(kmi.properties, name, False) for name in ["extend", "deselect", "center", "enumerate", "object"]]):
                            kmi.value = "PRESS"

                        elif kmi.properties.enumerate and not any([getattr(kmi.properties, name, False) for name in ["extend", "deselect", "toggle", "center", "object"]]):
                            kmi.value = "PRESS"

                        else:
                            kmi.active = False

                if kmi.idname == "transform.translate":
                    if kmi.map_type == "TWEAK":
                        kmi.active = False

                if kmi.idname == "view3d.view_axis":
                    if kmi.map_type == "TWEAK":
                        kmi.active = False

                if kmi.idname == "transform.tosphere":
                    kmi.properties.value = 1

                # if kmi.idname == "wm.context_toggle":  # gizmo toggle
                    # kmi.active = False



            # 3D VIEW TOOLS

            km = kc.keymaps.get("3D View Tool: Object, Cursor")
            for kmi in km.keymap_items:
                if kmi.idname == "view3d.cursor3d":
                    kmi.active = False

                if kmi.idname == "transform.translate":
                    kmi.active = False


            # OBJECT MODE

            km = kc.keymaps.get("Object Mode")
            for kmi in km.keymap_items:
                if kmi.idname == "object.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False


            # MESH

            km = kc.keymaps.get("Mesh")
            for kmi in km.keymap_items:
                if kmi.idname == "mesh.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False

                if kmi.idname == "mesh.edge_face_add" and kmi.type == "F":
                    kmi.active = False

                if kmi.idname == "mesh.select_mode" and kmi.type in ["ONE", "TWO", "THREE"]:
                    kmi.active = False

                if kmi.idname == "mesh.loop_select":
                    if not any([getattr(kmi.properties, name, False) for name in ["extend", "deselect", "toggle", "ring"]]):
                        kmi.value = "PRESS"
                        kmi.alt = True
                        kmi.properties.toggle = True

                    else:
                        kmi.active = False

                if kmi.idname == "mesh.edgering_select":
                    if kmi.properties.ring and not any([getattr(kmi.properties, name, False) for name in ["extend", "deselect", "toggle"]]):
                        kmi.value = "PRESS"
                        kmi.shift = False
                        kmi.properties.toggle = True

                    else:
                        kmi.active = False

                if kmi.idname == "mesh.shortest_path_pick":
                    kmi.value = "PRESS"

                if kmi.idname == "mesh.select_more":
                    kmi.type = "WHEELUPMOUSE"
                    kmi.shift = True
                    kmi.ctrl = False

                if kmi.idname == "mesh.select_less":
                    kmi.type = "WHEELDOWNMOUSE"
                    kmi.shift = True
                    kmi.ctrl = False

                if kmi.idname == "mesh.select_next_item":
                    kmi.type = "WHEELUPMOUSE"
                    kmi.shift = False

                if kmi.idname == "mesh.select_prev_item":
                    kmi.type = "WHEELDOWNMOUSE"
                    kmi.shift = False

                if kmi.idname == "mesh.select_linked":
                    kmi.active = False

                if kmi.idname == "mesh.select_linked_pick":
                    kmi.type = "LEFTMOUSE"
                    kmi.value = "DOUBLE_CLICK"
                    # kmi.properties.delimit = {"SHARP"}  # you can't set this as default and still remember the ops previous parameers, if you run it a second time

                    if kmi.properties.deselect:
                        kmi.alt = True
                    else:
                        kmi.shift = True

                if kmi.idname == "object.subdivision_set":
                    kmi.active = False


            # CURVE

            km = kc.keymaps.get("Curve")
            for kmi in km.keymap_items:
                if kmi.idname == "curve.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False


            # ARMATURE

            km = kc.keymaps.get("Armature")
            for kmi in km.keymap_items:
                if kmi.idname == "armature.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False


            # POSE

            km = kc.keymaps.get("Pose")
            for kmi in km.keymap_items:
                if kmi.idname == "pose.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False


            # UV

            km = kc.keymaps.get("UV Editor")
            for kmi in km.keymap_items:
                if kmi.idname == "uv.select_all":
                    if kmi.properties.action == "SELECT":
                        kmi.properties.action = "TOGGLE"

                    elif kmi.properties.action == "DESELECT":
                        kmi.active = False

        def add_keymaps(kc):
            # MESH
            km = kc.keymaps.get("Mesh")

            kmi = km.keymap_items.new("mesh.loop_multi_select", "LEFTMOUSE", "CLICK_DRAG", alt=True)
            kmi.properties.ring = False

            kmi = km.keymap_items.new("mesh.loop_multi_select", "LEFTMOUSE", "CLICK_DRAG", alt=True, ctrl=True)
            kmi.properties.ring = True

            kmi = km.keymap_items.new("mesh.subdivide", "TWO", "PRESS", alt=True)
            kmi.properties.smoothness = 1

            kmi = km.keymap_items.new("mesh.bridge_edge_loops", "TWO", "PRESS", ctrl=True)

        print("\n» Customizing 2.7x Keymap")

        kc = context.window_manager.keyconfigs.user

        modify_keymaps(kc)

        add_keymaps(kc)

        m3.M3_prefs().custom_keymaps = False

    def preferences(self, context):
        prefs = context.user_preferences

        if m3.M3_prefs().custom_preferences_interface:
            print("\n» Changing Preferences: Interface")

            v = prefs.view

            v.show_tooltips_python = True
            v.show_developer_ui = True
            v.mini_axis_type = "MINIMAL"

            v.use_zoom_to_mouse = True
            if m3.M3_prefs().obj_mode_rotate_around_active:
                v.use_rotate_around_active = True

            v.pie_animation_timeout = 0
            v.show_splash = False
            v.use_quit_dialog = False


        if m3.M3_prefs().custom_preferences_editing:
            print("\n» Changing Preferences: Editing")

            e = prefs.edit

            e.undo_steps = 64


        if m3.M3_prefs().custom_preferences_input:
            print("\n» Changing Preferences: Input")

            i = prefs.inputs

            i.invert_mouse_zoom = True

            blenderbinary = bpy.app.binary_path
            keymappath = os.path.join(os.path.dirname(blenderbinary), "2.80", "scripts", "presets", "keyconfig", "blender_27x.py")
            bpy.ops.wm.keyconfig_activate(filepath=keymappath)

            kcprefs = context.window_manager.keyconfigs.active.preferences
            kcprefs.select_mouse = "LEFT"

            # for some weird reason doing this 2 times is rquired if you edit the keymaps afterwards
            # otherwise left mouse tools be right mouse, could be a blender bug, TODO: investiage in beta phase
            bpy.ops.wm.keyconfig_activate(filepath=keymappath)

            kcprefs = context.window_manager.keyconfigs.active.preferences
            kcprefs.select_mouse = "LEFT"


        if m3.M3_prefs().custom_preferences_file:
            print("\n» Changing Preferences: File")

            f = prefs.filepaths

            f.use_file_compression = True
            f.use_load_ui = False
            f.save_version = 3
            f.recent_files = 20


        if m3.M3_prefs().custom_preferences_system:
            print("\n» Changing Preferences: System")

            c = prefs.addons['cycles'].preferences

            c.compute_device_type = "CUDA"
            for d in c.devices:
                d.use = True

            s = prefs.system

            s.opensubdiv_compute_type = "GLSL_COMPUTE"

            s.select_method = "GL_QUERY"

            s.anisotropic_filter = "FILTER_8"
            s.multi_sample = "8"

            s.text_hinting = "NONE"

            s.color_picker_type = "SQUARE_SV"

    def overlays(self, context):
        print("\n» Modifying Overlays")

        ws = context.workspace

        overlay = False
        for screen in ws.screens:
            if not overlay:
                for area in screen.areas:
                    if area.type == "VIEW_3D":
                        overlay = area.spaces[0].overlay

        if overlay:
            overlay.show_face_center = True
            overlay.show_backface_culling = True

    def matcaps(self, context, resourcespath, datafilespath):
        print("\n» Adding Matcaps")

        matcapsourcepath = os.path.join(resourcespath, "matcaps")
        matcaptargetpath = m3.makedir(os.path.join(datafilespath, "studiolights", "matcap"))
        matcaps = os.listdir(matcapsourcepath)

        for matcap in sorted(matcaps):
            shutil.copy(os.path.join(matcapsourcepath, matcap), matcaptargetpath)
            print("  %s -> %s" % (matcap, matcaptargetpath))

        context.user_preferences.studio_lights.refresh()

        if all([mc in matcaps for mc in ["matcap_base.exr", "matcap_shiny_red.exr"]]):
            m3.M3_prefs().switchmatcap1 = "matcap_base.exr"
            m3.M3_prefs().switchmatcap2 = "matcap_shiny_red.exr"


            print("\n» Setting up Viewport Shading")

            ws = context.workspace

            shading = False
            for screen in ws.screens:
                if not shading:
                    for area in screen.areas:
                        if area.type == "VIEW_3D":
                            shading = area.spaces[0].shading

            if shading:
                shading.type = "SOLID"
                shading.light = "MATCAP"
                shading.studio_light = "matcap_base.exr"
                shading.color_type = "SINGLE"
                shading.single_color = (0.2270, 0.2270, 0.2423)  # hex 838387

                shading.cavity_ridge_factor = 0
                shading.cavity_valley_factor = 2

    def theme(self, scriptspath, resourcespath):
        print("\n» Enabling M3 theme")

        themesourcepath = os.path.join(resourcespath, "theme", "m3.xml")
        themetargetpath = m3.makedir(os.path.join(scriptspath, "presets", "interface_theme"))

        filepath = shutil.copy(themesourcepath, themetargetpath)
        bpy.ops.script.execute_preset(filepath=filepath, menu_idname="USERPREF_MT_interface_theme_presets")


class RestoreKeymaps(bpy.types.Operator):
    bl_idname = "machin3.restore_keymaps"
    bl_label = "MACHIN3: Restore Keymaps"
    bl_options = {'REGISTER'}

    def execute(self, context):
        kc = context.window_manager.keyconfigs.user

        for km in kc.keymaps:
            if km.is_user_modified:
                km.restore_to_default()

        m3.M3_prefs().dirty_keymaps = False

        return {'FINISHED'}
