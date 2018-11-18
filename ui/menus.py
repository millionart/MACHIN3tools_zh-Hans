import bpy
from ..utils import MACHIN3 as m3


class VIEW3D_MT_edit_mesh_machin3tools(bpy.types.Menu):
    bl_label = "(W)MACHIN3tools"

    # TODO: comp mode availability check

    def draw(self, context):
        mode = m3.get_mode()
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_QuickJoin:
            column.operator("machin3.quick_join_last", text="Quick Join (Last)")
        if m3.M3_prefs().activate_QuickJoin:
            column.operator("machin3.quick_join_center", text="Quick Join (Center)")
        if m3.M3_prefs().activate_SmartModes:
            column.operator("machin3.smart_modes", text="Smart Modes")
        if m3.M3_prefs().activate_StarConnect:
            column.operator("machin3.star_connect", text="Star Connect")
        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_MoreSmartModes:
            column.operator("machin3.more_smart_modes", text="More Smart Modes")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_SlideExtend:
            if mode == "VERT":
                column.operator("machin3.slide_extend", text="Slide Extend")
        if m3.M3_prefs().activate_SurfaceSlide:
            column.operator("machin3.surface_slide", text="Surface Slide")
        if m3.M3_prefs().activate_EdgeLength:
            column.operator("machin3.edge_length", text="Edge Length")
        if m3.M3_prefs().activate_Emboss:
            if mode == "FACE":
                column.operator("machin3.emboss", text="Emboss")


class VIEW3D_MT_object_machin3tools(bpy.types.Menu):
    bl_label = "(W)MACHIN3tools"

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_Align:
            column.operator("machin3.align", text="Align")
        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_CenterCube:
            column.operator("machin3.center_cube", text="Center Cube")
        if m3.M3_prefs().activate_CleanoutMaterials:
            column.operator("machin3.cleanout_materials", text="Cleanout Materials")
        if m3.M3_prefs().activate_CleanoutUVs:
            column.operator("machin3.cleanout_uvs", text="Cleanout UVs")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_LockItAll:
            column.operator("machin3.lock_it_all", text="Lock It All")
        if m3.M3_prefs().activate_HideMeshes:
            column.operator("machin3.hide_meshes", text="Hide Meshes")
        if m3.M3_prefs().activate_ModMachine:
            column.operator("machin3.mod_machine", text="Mod Machine")
        if m3.M3_prefs().activate_CameraHelper:
            column.operator("machin3.camera_helper", text="Camera Helper")
        if m3.M3_prefs().activate_Hierarch:
            column.operator("machin3.hierarch", text="Hierarch")
        if m3.M3_prefs().activate_FlipNormals:
            column.operator("machin3.flip_normals", text="Flip Normals")
        if m3.M3_prefs().activate_SymmetrizeGPencil:
            if context.gpencil_data:
                column.operator("machin3.symmetrize_gpencil", text="Symmetrize GPencil")


class MenuAppendMaterials(bpy.types.Menu):
    bl_idname = "MACHIN3_MT_append_materials"
    bl_label = "Append Materials"

    def draw(self, context):
        layout = self.layout

        names = [mat.name for mat in m3.M3_prefs().appendmats]

        if names:
            names.insert(0, "ALL")
        else:
            layout.label("No Materials added yet!", icon="ERROR")
            layout.label("Check MACHIN3tools prefs.", icon="INFO")


        for name in names:

            if name == "ALL":
                layout.operator("machin3.append_material", text=name, icon="MATERIAL_DATA").name = name
                layout.separator()
            else:
                n = name.replace("-", "")
                mat = bpy.data.materials.get(n)
                icon_val = layout.icon(mat) if mat else 0

                layout.operator("machin3.append_material", text=n, icon_value=icon_val).name = n

            if name.endswith("-"):
                layout.separator()
