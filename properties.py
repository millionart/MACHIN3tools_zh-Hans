import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty


class M3SceneProperties(bpy.types.PropertyGroup):
    """
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

    """

    def update_occlude_geometry(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.occlude_geometry
        shading.xray_alpha = 1

    def update_show_edit_mesh_wire(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.show_edit_mesh_wire
        shading.xray_alpha = 0.1


    occlude_geometry: BoolProperty(name="Occlude Geometry", default=False, update=update_occlude_geometry)
    show_edit_mesh_wire: BoolProperty(name="Show Edit Mesh Wireframe", default=False, update=update_show_edit_mesh_wire)


class AppendMatsUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.split(factor=0.7)
        row.label(text=item.name)


class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
