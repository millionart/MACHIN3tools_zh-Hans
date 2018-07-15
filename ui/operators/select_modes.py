import bpy
from ... utils import MACHIN3 as m3


class SelectEditObjectMode(bpy.types.Operator):
    bl_idname = "machin3.select_edit_object_mode"
    bl_label = "Class Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")

            # if bpy.context.scene.machin3.pieobjecteditmodeshow:
                # m3.unhide_all("MESH")
                # if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    # m3.unselect_all("MESH")
            # if bpy.context.scene.machin3.pieobjecteditmodetoggleao:
                # bpy.context.space_data.fx_settings.use_ssao = False

        else:
            bpy.ops.object.mode_set(mode="OBJECT")

        """
        else:
            if bpy.context.scene.machin3.pieobjecteditmodehide:
                # TODO: why does this sometimes occur?
                # Traceback (most recent call last):
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/ui/pie.py", line 453, in execute
                    # m3.hide_all("MESH")
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/M3utils.py", line 54, in hide_all
                    # select_all(string)
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/M3utils.py", line 32, in select_all
                    # bpy.ops.mesh.select_all(action='SELECT')
                  # File "/opt/Blender 2.78c/2.78/scripts/modules/bpy/ops.py", line 189, in __call__
                    # ret = op_call(self.idname_py(), None, kw)
                # RuntimeError: Operator bpy.ops.mesh.select_all.poll() failed, context is incorrect
                try:
                    m3.hide_all("MESH")
                except:
                    pass
            bpy.ops.object.mode_set(mode="OBJECT")

            # if bpy.context.scene.machin3.pieobjecteditmodetoggleao:
                # bpy.context.space_data.fx_settings.use_ssao = True
        """
        return {'FINISHED'}


class SelectVertexMode(bpy.types.Operator):
    bl_idname = "machin3.select_vertex_mode"
    bl_label = "Class Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

            # if bpy.context.scene.machin3.pieobjecteditmodeshow:
                # m3.unhide_all("MESH")

                # if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    # m3.unselect_all("MESH")

        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        # if bpy.context.scene.machin3.pieobjecteditmodetoggleao:
            # bpy.context.space_data.fx_settings.use_ssao = False
        return {'FINISHED'}


class SelectEdgeMode(bpy.types.Operator):
    bl_idname = "machin3.select_edge_mode"
    bl_label = "Class Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')

            # if bpy.context.scene.machin3.pieobjecteditmodeshow:
                # m3.unhide_all("MESH")

                # if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    # m3.unselect_all("MESH")

        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')

        # if bpy.context.scene.machin3.pieobjecteditmodetoggleao:
            # bpy.context.space_data.fx_settings.use_ssao = False
        return {'FINISHED'}


class SelectFaceMode(bpy.types.Operator):
    bl_idname = "machin3.select_face_mode"
    bl_label = "Class Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

            # if bpy.context.scene.machin3.pieobjecteditmodeshow:
                # m3.unhide_all("MESH")
                # if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    # m3.unselect_all("MESH")
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

        # if bpy.context.scene.machin3.pieobjecteditmodetoggleao:
            # bpy.context.space_data.fx_settings.use_ssao = False
        return {'FINISHED'}
