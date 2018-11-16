import bpy
from ... utils import MACHIN3 as m3


class EditMode(bpy.types.Operator):
    bl_idname = "machin3.edit_mode"
    bl_label = "Edit Mode"
    bl_options = {'REGISTER'}

    def execute(self, context):

        if context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")


        elif context.mode == "EDIT_MESH":
            shading = context.space_data.shading
            shading.show_xray = False

            bpy.ops.object.mode_set(mode="OBJECT")

        return {'FINISHED'}


class VertexMode(bpy.types.Operator):
    bl_idname = "machin3.vertex_mode"
    bl_label = "Vertex Mode"
    bl_description = "Vertex Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='VERT')

        return {'FINISHED'}


class EdgeMode(bpy.types.Operator):
    bl_idname = "machin3.edge_mode"
    bl_label = "Edge Mode"
    bl_description = "Edge Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='EDGE')

        return {'FINISHED'}


class FaceMode(bpy.types.Operator):
    bl_idname = "machin3.face_mode"
    bl_label = "Face Mode"
    bl_description = "Face Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='FACE')

        return {'FINISHED'}
