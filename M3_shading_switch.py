bl_info = {
    "name": "Shading Switch",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu/Shift + Mouse Button 5. Z for switching to Wireframe and back.",
    "description": "Switches between Material and Solid shading modes. Also re-assigns Z key for wireframe switching and Shift + Z for render switching accordingly.",
    "warning": "",
    "wiki_url": "",
    "category": "Interface"}

# SETTINGS

button = "BUTTON5MOUSE"
press = "PRESS"
ctrl = False
alt = False
shift = True

button2 = "Z"

import bpy


class ShadingSwitch(bpy.types.Operator):
    bl_idname = "machin3.shading_switch"
    bl_label = "MACHIN3: Shading Switch"

    def execute(self, context):
        shadingmode = bpy.context.space_data.viewport_shade

        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

        print("\n----- MACHIN3: Shading Switch -----")

        if shadingmode == "SOLID":
            bpy.context.space_data.viewport_shade = "MATERIAL"
            print("Switched to MATERIAL shading mode.")

            kmi = km.keymap_items.new('wm.context_toggle_enum', button2, 'PRESS')
            kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            kmi_props_setattr(kmi.properties, 'value_1', 'MATERIAL')
            kmi_props_setattr(kmi.properties, 'value_2', 'WIREFRAME')
            print("'%s' key now switches between MATERIAL and WIREFRAME." % (button2))

            kmi = km.keymap_items.new('wm.context_toggle_enum', button2, 'PRESS', shift=True)
            kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            kmi_props_setattr(kmi.properties, 'value_1', 'MATERIAL')
            kmi_props_setattr(kmi.properties, 'value_2', 'RENDERED')
            print("Shift + '%s' key now switches between MATERIAL and RENDERED." % (button2))
        elif shadingmode == "MATERIAL":
            bpy.context.space_data.viewport_shade = "SOLID"
            print("Switched to SOLID shading mode.")

            kmi = km.keymap_items.new('wm.context_toggle_enum', button2, 'PRESS')
            kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            kmi_props_setattr(kmi.properties, 'value_1', 'SOLID')
            kmi_props_setattr(kmi.properties, 'value_2', 'WIREFRAME')
            print("'%s' key now switches between SOLID and WIREFRAME." % (button2))

            kmi = km.keymap_items.new('wm.context_toggle_enum', button2, 'PRESS', shift=True)
            kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
            kmi_props_setattr(kmi.properties, 'value_1', 'SOLID')
            kmi_props_setattr(kmi.properties, 'value_2', 'RENDERED')
            print("Shift + '%s' key now switches between SOLID and RENDERED." % (button2))

        return {'FINISHED'}


def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


def register():
    bpy.utils.register_class(ShadingSwitch)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new(ShadingSwitch.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(ShadingSwitch)

    # TODO: properly unregister keymap and keymap_items


if __name__ == "__main__":
    register()
