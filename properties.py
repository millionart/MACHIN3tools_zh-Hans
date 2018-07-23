import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)

    pieobjecteditmodehide = BoolProperty(name="Auto Hide", default=False)
    pieobjecteditmodeshow = BoolProperty(name="Auto Reveal", default=False)
    pieobjecteditmodeshowunselect = BoolProperty(name="Unselect", default=False)
    pieobjecteditmodetoggleao = BoolProperty(name="Toggle AO", default=False)

    pieviewsalignactive = bpy.props.BoolProperty(name="Align Active", default=False)

    preview_percentage = IntProperty(name="Preview Percentage", default=100, min=10, max=100, subtype="PERCENTAGE")
    final_percentage = IntProperty(name="Final Percentage", default=250, min=100, max=1000, subtype="PERCENTAGE")

    preview_samples = IntProperty(name="Preview Percentage", default=32, min=12, max=64)
    final_samples = IntProperty(name="Final Percentage", default=256, min=64, max=2048)


class AppendMatsUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.split(0.7)
        row.label(text=item.name)


class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
