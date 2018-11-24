import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty


# COLLECTIONS

class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()


class HistoryObjectsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Object", type=bpy.types.Object)


class HistoryUnmirroredCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Unmirror", type=bpy.types.Object)


class HistoryEpochCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    objects: CollectionProperty(type=HistoryObjectsCollection)
    unmirrored: CollectionProperty(type=HistoryUnmirroredCollection)


# SCENE PROPERTIES


class M3SceneProperties(bpy.types.PropertyGroup):
    def update_pass_through(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.pass_through
        shading.xray_alpha = 1

    def update_show_edit_mesh_wire(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.show_edit_mesh_wire
        shading.xray_alpha = 0.1

    def update_uv_sync_select(self, context):
        toolsettings = context.scene.tool_settings
        toolsettings.use_uv_select_sync = self.uv_sync_select

        if not toolsettings.use_uv_select_sync:
            bpy.ops.mesh.select_all(action="SELECT")


    pass_through: BoolProperty(name="Pass Through", default=False, update=update_pass_through)
    show_edit_mesh_wire: BoolProperty(name="Show Edit Mesh Wireframe", default=False, update=update_show_edit_mesh_wire)
    uv_sync_select: BoolProperty(name="Synce Selection", default=False, update=update_uv_sync_select)

    focus_history: CollectionProperty(type=HistoryEpochCollection)
