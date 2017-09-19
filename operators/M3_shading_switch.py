import bpy
from bpy.props import StringProperty
from .. import M3utils as m3
from .. import developer_utils as du


# TODO: ShadingSwitch() must call prepare_for_viewport_shading() when switching from solid to material shading


class ShadingSwitch(bpy.types.Operator):
    bl_idname = "machin3.shading_switch"
    bl_label = "MACHIN3: Shading Switch"
    bl_options = {'REGISTER'}

    def execute(self, context):
        shadingmode = bpy.context.space_data.viewport_shade

        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

        print("\n----- MACHIN3: Shading Switch -----")

        if shadingmode == "SOLID":
            bpy.context.space_data.viewport_shade = "MATERIAL"
            print("Switched to MATERIAL shading mode.")

            kmi = km.keymap_items.new('machin3.toggle_wireframe', "Z", 'PRESS')
            du.kmi_props_setattr(kmi.properties, 'shading', 'MATERIAL')
            print("'%s' key now switches between MATERIAL and WIREFRAME." % ("Z"))

            kmi = km.keymap_items.new('machin3.toggle_rendered', "Z", 'PRESS', shift=True)
            du.kmi_props_setattr(kmi.properties, 'shading', 'MATERIAL')
            print("Shift + '%s' key now switches between MATERIAL and RENDERED." % ("Z"))
        elif shadingmode == "MATERIAL":
            bpy.context.space_data.viewport_shade = "SOLID"
            print("Switched to SOLID shading mode.")

            kmi = km.keymap_items.new('machin3.toggle_wireframe', "Z", 'PRESS')
            du.kmi_props_setattr(kmi.properties, 'shading', 'SOLID')
            print("'%s' key now switches between SOLID and WIREFRAME." % ("Z"))

            kmi = km.keymap_items.new('machin3.toggle_rendered', "Z", 'PRESS', shift=True)
            du.kmi_props_setattr(kmi.properties, 'shading', 'SOLID')
            print("Shift + '%s' key now switches between SOLID and RENDERED." % ("Z"))

        return {'FINISHED'}


class ToggleWireframe(bpy.types.Operator):
    bl_idname = "machin3.toggle_wireframe"
    bl_label = "MACHIN3: Toggle Wireframe"

    shading = StringProperty(name="Value", description="Toggle enum", maxlen=1024)

    def execute(self, context):
        bpy.ops.wm.context_toggle_enum(data_path="space_data.viewport_shade", value_1=self.shading, value_2="WIREFRAME")
        return {'FINISHED'}


class ToggleRendered(bpy.types.Operator):
    bl_idname = "machin3.toggle_rendered"
    bl_label = "MACHIN3: Toggle Rendered"

    shading = StringProperty(name="Value", description="Toggle enum", maxlen=1024)

    def execute(self, context):
        if bpy.app.version >= (2, 79, 0) and m3.M3_prefs().viewportcompensation:
            # print("Viewport Material Compensation normal switching")

            shadingmode = bpy.context.space_data.viewport_shade

            if shadingmode == "RENDERED":
                prepare_for_material_shading()
            else:
                prepare_for_rendering()

        bpy.ops.wm.context_toggle_enum(data_path="space_data.viewport_shade", value_1=self.shading, value_2="RENDERED")
        return {'FINISHED'}


class ResetMaterialViewportComensation(bpy.types.Operator):
    bl_idname = "machin3.reset_material_viewport_compensation"
    bl_label = "MACHIN3: Reset Material Viewport Compensation"

    def execute(self, context):
        if bpy.app.version >= (2, 79, 0):
            prepare_for_rendering()

        return {'FINISHED'}


def prepare_for_rendering():
    mode = m3.M3_prefs().shadingcompensation

    print("\nPreparing Materials for Rendering")

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    reset_principledpbr_node(mode, mat, node)
                elif node.type == "GROUP":
                    if "Decal" in node.node_tree.name:
                        for n in node.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                reset_principledpbr_node(mode, mat, n, node)


def reset_principledpbr_node(mode, material, node, group=None):
    try:
        if node["M3"]:
            ischanged = True
    except:
        ischanged = False

    if ischanged:  # reset changes and delete M3 id prop

        # Decal Material
        if group:
            groupname = group.node_tree.name
            if "Subset" in groupname:
                if node.name == "Principled BSDF":
                    metallic = group.inputs['Material Metallic']
                    roughness = group.inputs['Material Roughness']
                elif node.name == "Principled BSDF.001":
                    metallic = group.inputs['Subset Metallic']
                    roughness = group.inputs['Subset Roughness']
            elif "Subtractor" in groupname:
                metallic = group.inputs['Material Metallic']
                roughness = group.inputs['Material Roughness']
            elif "Panel" in groupname:
                if node.name == "Principled BSDF":
                    metallic = group.inputs['Material 1 Metallic']
                    roughness = group.inputs['Material 1 Roughness']
                elif node.name == "Principled BSDF.001":
                    metallic = group.inputs['Material 2 Metallic']
                    roughness = group.inputs['Material 2 Roughness']
            elif "Info" in groupname:
                metallic = group.inputs['Info Metallic']
                roughness = group.inputs['Info Roughness']

            transparent = group.node_tree.nodes.get("Transparent BSDF")
            transparent.inputs[0].default_value = (1, 1, 1, 1)

        # Non-Decal Material
        else:
            metallic = node.inputs[4]
            roughness = node.inputs[7]

        metallic.default_value = node["M3"]["metallic"]
        roughness.default_value = node["M3"]["roughness"]

        del node["M3"]

        # print("Material: '%s', Node: '%s' - Reset PBR values and deleted M3 ID Property" % (material.name, node.name))
    else:
        # print("Material: '%s', Node: '%s' - No M3 ID Property found" % (material.name, node.name))
        pass


def prepare_for_material_shading():
    mode = m3.M3_prefs().shadingcompensation

    print("\nPreparing Materials for Viewport Display")

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    adjust_principledpbr_node(mode, mat, node)
                elif node.type == "GROUP":
                    if "Decal" in node.node_tree.name:
                        for n in node.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                adjust_principledpbr_node(mode, mat, n, node)


def adjust_principledpbr_node(mode, material, node, group=None):
    targetmetallic = m3.M3_prefs().targetmetallic
    secondarytargetmetallic = m3.M3_prefs().secondarytargetmetallic
    targetroughness = m3.M3_prefs().targetroughness
    alphafix = m3.M3_prefs().alphafix

    # get render parameters

    # Decal Material
    if group:
        groupname = group.node_tree.name
        if "Subset" in groupname:
            if node.name == "Principled BSDF":
                color = group.inputs['Material Color'].links[0].from_socket
                metallic = group.inputs['Material Metallic']
                roughness = group.inputs['Material Roughness']
            elif node.name == "Principled BSDF.001":
                color = group.inputs['Subset Color'].links[0].from_socket
                metallic = group.inputs['Subset Metallic']
                roughness = group.inputs['Subset Roughness']
        elif "Subtractor" in groupname:
            color = group.inputs['Material Color'].links[0].from_socket
            metallic = group.inputs['Material Metallic']
            roughness = group.inputs['Material Roughness']
        elif "Panel" in groupname:
            if node.name == "Principled BSDF":
                color = group.inputs['Material 1 Color'].links[0].from_socket
                metallic = group.inputs['Material 1 Metallic']
                roughness = group.inputs['Material 1 Roughness']
            elif node.name == "Principled BSDF.001":
                color = group.inputs['Material 2 Color'].links[0].from_socket
                metallic = group.inputs['Material 2 Metallic']
                roughness = group.inputs['Material 2 Roughness']
        elif "Info" in groupname:
            color = node.inputs[0]  # color is irrelevant for info decals, as it comes from an image, we just need it for the dict below
            metallic = group.inputs['Info Metallic']
            roughness = group.inputs['Info Roughness']

    # Non-Decal Material
    else:
        groupname = ""
        color = node.inputs[0]
        metallic = node.inputs[4]
        roughness = node.inputs[7]

    # save render parameters
    node["M3"] = {"color": color.default_value,
                  "metallic": metallic.default_value,
                  "roughness": roughness.default_value}

    # print("Material: '%s', Node: '%s' - Set M3 ID Property" % (material.name, node.name))

    # set viewport parameters
    if mode == "278":  # this mode mirrors the look in 2.78, very rough and without metallic darkening
        metallic.default_value = 0.5
        roughness.default_value = 1
    elif mode == "279":  # this mode lerps between render values and target values based on the metallic amount and color average

        if "Info" in groupname:
            metallic.default_value = m3.lerp(metallic.default_value, targetmetallic, metallic.default_value)
            roughness.default_value = m3.lerp(roughness.default_value, targetroughness, metallic.default_value)
        else:
            coloravg = (color.default_value[0] + color.default_value[1] + color.default_value[2]) / 3

            metallic.default_value = m3.lerp(m3.lerp(metallic.default_value, targetmetallic, metallic.default_value), secondarytargetmetallic, coloravg)
            roughness.default_value = m3.lerp(roughness.default_value, targetroughness, metallic.default_value)

    if group:
        if mode == "279" and alphafix:
            transparent = group.node_tree.nodes.get("Transparent BSDF")
            transparent.inputs[0].default_value = (0, 0, 0, 1)
