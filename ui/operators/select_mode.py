import bpy
from ... utils import MACHIN3 as m3


class ToggleEditMode(bpy.types.Operator):
    bl_idname = "machin3.toggle_edit_mode"
    bl_label = "Toggle Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")


        elif context.mode == "EDIT_MESH":
            shading = context.space_data.shading
            shading.show_xray = False

            bpy.ops.object.mode_set(mode="OBJECT")

        return {'FINISHED'}


class SelectVertexMode(bpy.types.Operator):
    bl_idname = "machin3.select_vertex_mode"
    bl_label = "Vertex Mode"
    bl_description = "Vertex Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='VERT')

        return {'FINISHED'}


class SelectEdgeMode(bpy.types.Operator):
    bl_idname = "machin3.select_edge_mode"
    bl_label = "Edge Mode"
    bl_description = "Edge Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='EDGE')

        return {'FINISHED'}


class SelectFaceMode(bpy.types.Operator):
    bl_idname = "machin3.select_face_mode"
    bl_label = "Face Mode"
    bl_description = "Face Select\nCTRL + Click: Expand Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type='FACE')

        return {'FINISHED'}
