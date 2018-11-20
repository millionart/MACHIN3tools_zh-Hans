import bpy
from ..utils import MACHIN3 as m3



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
