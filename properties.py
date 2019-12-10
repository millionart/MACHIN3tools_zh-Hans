import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty
from . items import eevee_preset_items


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
    def update_xray(self, context):
        x = (self.pass_through, self.show_edit_mesh_wire)
        shading = context.space_data.shading

        shading.show_xray = True if any(x) else False

        if self.show_edit_mesh_wire:
            shading.xray_alpha = 0.1

        elif self.pass_through:
            shading.xray_alpha = 1 if context.active_object and context.active_object.type == "MESH" else 0.5

    def update_uv_sync_select(self, context):
        toolsettings = context.scene.tool_settings
        toolsettings.use_uv_select_sync = self.uv_sync_select

        if not toolsettings.use_uv_select_sync:
            bpy.ops.mesh.select_all(action="SELECT")

    def update_show_cavity(self, context):
        t = (self.show_cavity, self.show_curvature)
        shading = context.space_data.shading

        shading.show_cavity = True if any(t) else False

        if t == (True, True):
            shading.cavity_type = "BOTH"

        elif t == (True, False):
            shading.cavity_type = "WORLD"

        elif t == (False, True):
            shading.cavity_type = "SCREEN"

    def update_grouppro_dotnames(self, context):
        gpcols = [col for col in bpy.data.collections if col.created_with_gp]

        for col in gpcols:
            # hide collections
            if self.grouppro_dotnames:
                if not col.name.startswith("."):
                    col.name = ".%s" % col.name

            else:
                if col.name.startswith("."):
                    col.name = col.name[1:]

    pass_through: BoolProperty(name="Pass Through", default=False, update=update_xray)
    show_edit_mesh_wire: BoolProperty(name="Show Edit Mesh Wireframe", default=False, update=update_xray)
    uv_sync_select: BoolProperty(name="Synce Selection", default=False, update=update_uv_sync_select)

    show_cavity: BoolProperty(name="Cavity", default=True, update=update_show_cavity)
    show_curvature: BoolProperty(name="Curvature", default=False, update=update_show_cavity)

    focus_history: CollectionProperty(type=HistoryEpochCollection)

    grouppro_dotnames: BoolProperty(name=".dotname GroupPro collections", default=False, update=update_grouppro_dotnames)


    def update_eevee_preset(self, context):
        eevee = context.scene.eevee
        shading = context.space_data.shading

        if self.eevee_preset == 'NONE':
            eevee.use_ssr = False
            eevee.use_gtao = False
            eevee.use_bloom = False
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = False

        elif self.eevee_preset == 'LOW':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = True
            eevee.use_ssr_refraction = False
            eevee.use_gtao = True
            eevee.use_bloom = False
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = True

        elif self.eevee_preset == 'HIGH':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = False
            eevee.use_ssr_refraction = True
            eevee.use_gtao = True
            eevee.use_bloom = True
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = True

        elif self.eevee_preset == 'ULTRA':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = False
            eevee.use_ssr_refraction = True
            eevee.use_gtao = True
            eevee.use_bloom = True
            eevee.use_volumetric_lights = True

            shading.use_scene_lights = True

    def update_eevee_gtao_factor(self, context):
        context.scene.eevee.gtao_factor = self.eevee_gtao_factor

    def update_eevee_bloom_intensity(self, context):
        context.scene.eevee.bloom_intensity = self.eevee_bloom_intensity

    eevee_preset: EnumProperty(name="Eevee Preset", description="Eevee Quality Presets", items=eevee_preset_items, default='NONE', update=update_eevee_preset)
    eevee_gtao_factor: FloatProperty(name="Factor", default=1, min=0, step=0.1, update=update_eevee_gtao_factor)
    eevee_bloom_intensity: FloatProperty(name="Intensity", default=0.05, min=0, step=0.1, update=update_eevee_bloom_intensity)

    object_axes_size: FloatProperty(name="Object Axes Size", default=0.3, min=0)
    object_axes_alpha: FloatProperty(name="Object Axes Alpha", default=0.75, min=0, max=1)
