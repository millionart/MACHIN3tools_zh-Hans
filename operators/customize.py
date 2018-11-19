import bpy
import os
import shutil
from .. utils import MACHIN3 as m3


# TODO: do the prefs part based on a dictionary?


class Customize(bpy.types.Operator):
    bl_idname = "machin3.customize"
    bl_label = "MACHIN3: Customize"
    bl_options = {'REGISTER'}

    def execute(self, context):
        os.system("clear")

        scriptspath = bpy.utils.user_resource('SCRIPTS')
        datafilespath = bpy.utils.user_resource('DATAFILES')

        resourcespath = os.path.join(m3.M3_prefs().path, "resources")

        # WINDOW (is read only)
        # bpy.context.window.screen.areas[0].regions[0].alignment = "TOP"
        # bpy.context.area.region[0].alignment = "TOP"

        # SET CURSOR TOOL
        bpy.ops.wm.tool_set_by_name(name="Cursor")

        # THEME
        self.theme(scriptspath, resourcespath)

        # MATCAPS + DEFAULT SHADING
        self.matcaps(context, resourcespath, datafilespath)

        # OVERLAYS
        self.overlays(context)

        # PREFERENCES
        # self.preferences(context)

        # CUSTOM KEYMAP

        # TODO

        return {'FINISHED'}

    def preferences(self, context):
        prefs = context.user_preferences

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


        print("\n» Changing Preferences: Editing")

        e = prefs.edit

        e.undo_steps = 64


        print("\n» Changing Preferences: Input")

        i = prefs.inputs

        blenderbinary = bpy.app.binary_path
        keymappath = os.path.join(os.path.dirname(blenderbinary), "2.80", "scripts", "presets", "keyconfig", "blender_27x.py")
        bpy.ops.wm.keyconfig_activate(filepath=keymappath)

        i.select_mouse = "LEFT"
        i.invert_mouse_zoom = True


        print("\n» Changing Preferences: File")

        f = prefs.filepaths

        f.use_file_compression = True
        f.use_load_ui = False
        f.save_version = 3
        f.recent_files = 20


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

        overlay = context.space_data.overlay

        overlay.show_face_center = True
        overlay.show_backface_culling = True

    def matcaps(self, context, resourcespath, datafilespath):
        print("\n» Adding Matcaps")

        matcapsourcepath = os.path.join(resourcespath, "matcap")
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

            shading = context.space_data.shading

            shading.type = "SOLID"
            shading.light = "MATCAP"
            shading.studio_light = "matcap_base.exr"
            shading.color_type = "SINGLE"
            shading.single_color = (0.2270, 0.2270, 0.2423)  # hex 838387

    def theme(self, scriptspath, resourcespath):
        print("\n» Enabllng M3 theme")

        themesourcepath = os.path.join(resourcespath, "theme", "m3.xml")
        themetargetpath = m3.makedir(os.path.join(scriptspath, "presets", "interface_theme"))

        filepath = shutil.copy(themesourcepath, themetargetpath)
        bpy.ops.script.execute_preset(filepath=filepath, menu_idname="USERPREF_MT_interface_theme_presets")
