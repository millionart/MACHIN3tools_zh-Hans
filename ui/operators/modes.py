import bpy
from bpy.props import StringProperty
from ... utils import MACHIN3 as m3


# TODO: cavity toggle


class EditMode(bpy.types.Operator):
    bl_idname = "machin3.edit_mode"
    bl_label = "Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        viewprefs = context.user_preferences.view
        shading = context.space_data.shading

        rotate_around_active = m3.M3_prefs().obj_mode_rotate_around_active
        toggle_cavity = m3.M3_prefs().toggle_cavity

        if context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")

            if rotate_around_active:
                viewprefs.use_rotate_around_active = False

            if toggle_cavity:
                shading.show_cavity = False


        elif context.mode == "EDIT_MESH":
            shading = context.space_data.shading
            shading.show_xray = False

            bpy.ops.object.mode_set(mode="OBJECT")

            if rotate_around_active:
                viewprefs.use_rotate_around_active = True

            if toggle_cavity:
                shading.show_cavity = True

        return {'FINISHED'}


class VertexMode(bpy.types.Operator):
    bl_idname = "machin3.vertex_mode"
    bl_label = "Vertex Mode"
    bl_description = "Vertex Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='VERT')


        if m3.M3_prefs().obj_mode_rotate_around_active:
            context.user_preferences.view.use_rotate_around_active = False

        if m3.M3_prefs().toggle_cavity:
            context.space_data.shading.show_cavity = False

        return {'FINISHED'}


class EdgeMode(bpy.types.Operator):
    bl_idname = "machin3.edge_mode"
    bl_label = "Edge Mode"
    bl_description = "Edge Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='EDGE')


        if m3.M3_prefs().obj_mode_rotate_around_active:
            context.user_preferences.view.use_rotate_around_active = False

        if m3.M3_prefs().toggle_cavity:
            context.space_data.shading.show_cavity = False

        return {'FINISHED'}


class FaceMode(bpy.types.Operator):
    bl_idname = "machin3.face_mode"
    bl_label = "Face Mode"
    bl_description = "Face Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='FACE')


        if m3.M3_prefs().obj_mode_rotate_around_active:
            context.user_preferences.view.use_rotate_around_active = False


        if m3.M3_prefs().toggle_cavity:
            context.space_data.shading.show_cavity = False

        return {'FINISHED'}


class ImageMode(bpy.types.Operator):
    bl_idname = "machin3.image_mode"
    bl_label = "MACHIN3: Image Mode"
    bl_options = {'REGISTER'}

    mode: StringProperty()

    def execute(self, context):
        view = context.space_data
        active = context.active_object

        view.mode = self.mode

        if self.mode == "UV" and active:
            if active.mode == "OBJECT":
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")

        return {'FINISHED'}


class UVMode(bpy.types.Operator):
    bl_idname = "machin3.uv_mode"
    bl_label = "MACHIN3: UV Mode"
    bl_options = {'REGISTER'}

    mode: StringProperty()

    def execute(self, context):
        toolsettings = context.scene.tool_settings
        view = context.space_data

        if view.mode != "UV":
            view.mode = "UV"

        if toolsettings.use_uv_select_sync:
            bpy.ops.mesh.select_mode(type=self.mode.replace("VERTEX", "VERT"))

        else:
            toolsettings.uv_select_mode = self.mode

        return {'FINISHED'}
