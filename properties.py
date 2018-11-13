import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty



class M3HistoryObjectEntry(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Object", type=bpy.types.Object)


class M3HistoryUnmirrorEntry(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Unmirror", type=bpy.types.Object)


class M3HistoryEpoch(bpy.types.PropertyGroup):
    name: StringProperty()
    objects: CollectionProperty(type=M3HistoryObjectEntry)
    unmirrored: CollectionProperty(type=M3HistoryUnmirrorEntry)


class M3SceneProperties(bpy.types.PropertyGroup):
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

    focus_history: CollectionProperty(type=M3HistoryEpoch)



class AppendMatsUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.split(factor=0.7)
        row.label(text=item.name)


class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
