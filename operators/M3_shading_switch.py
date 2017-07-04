import bpy
from .. import M3utils as m3


class ShadingSwitch(bpy.types.Operator):
    bl_idname = "machin3.shading_switch"
    bl_label = "MACHIN3: Shading Switch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        shadingmode = bpy.context.space_data.viewport_shade

        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

        print("\n----- MACHIN3: Shading Switch -----")

        if shadingmode == "SOLID":
            bpy.context.space_data.viewport_shade = "MATERIAL"
            print("Switched to MATERIAL shading mode.")

            kmi = km.keymap_items.new('wm.context_toggle_enum', "Z", 'PRESS')
            m3.kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            m3.kmi_props_setattr(kmi.properties, 'value_1', 'MATERIAL')
            m3.kmi_props_setattr(kmi.properties, 'value_2', 'WIREFRAME')
            print("'%s' key now switches between MATERIAL and WIREFRAME." % ("Z"))

            kmi = km.keymap_items.new('wm.context_toggle_enum', "Z", 'PRESS', shift=True)
            m3.kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            m3.kmi_props_setattr(kmi.properties, 'value_1', 'MATERIAL')
            m3.kmi_props_setattr(kmi.properties, 'value_2', 'RENDERED')
            print("Shift + '%s' key now switches between MATERIAL and RENDERED." % ("Z"))
        elif shadingmode == "MATERIAL":
            bpy.context.space_data.viewport_shade = "SOLID"
            print("Switched to SOLID shading mode.")

            kmi = km.keymap_items.new('wm.context_toggle_enum', "Z", 'PRESS')
            m3.kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            m3.kmi_props_setattr(kmi.properties, 'value_1', 'SOLID')
            m3.kmi_props_setattr(kmi.properties, 'value_2', 'WIREFRAME')
            print("'%s' key now switches between SOLID and WIREFRAME." % ("Z"))

            kmi = km.keymap_items.new('wm.context_toggle_enum', "Z", 'PRESS', shift=True)
            m3.kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            m3.kmi_props_setattr(kmi.properties, 'value_1', 'SOLID')
            m3.kmi_props_setattr(kmi.properties, 'value_2', 'RENDERED')
            print("Shift + '%s' key now switches between SOLID and RENDERED." % ("Z"))

        return {'FINISHED'}
