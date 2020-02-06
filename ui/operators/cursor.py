import bpy
import bmesh
from ... utils.math import create_rotation_matrix_from_normal, get_center_between_verts, create_rotation_matrix_from_edge
from ... utils.scene import set_cursor


class CursorToOrigin(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_origin"
    bl_label = "MACHIN3: Cursor to Origin"
    bl_description = "Reset Cursor location and rotation to world origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_cursor()
        return {'FINISHED'}


class CursorToSelected(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_selected"
    bl_label = "MACHIN3: Cursor to Selected"
    bl_description = "Set Cursor location and rotation to selected object or mesh element"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object or context.selected_objects

    def execute(self, context):
        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        # make sure the is an active
        if sel and not active:
            context.view_layer.objects.active = sel[0]
            sel.remove(active)

        # initiate bool used for using Blender's op as a fallback
        is_cursor_set = False

        # if in object mode with multiple selected ojects, pass it on to Blender's op
        if context.mode == 'OBJECT' and active and not sel:
            self.cursor_to_active_object(active)
            is_cursor_set = True

        elif context.mode == 'EDIT_MESH':
            is_cursor_set = self.cursor_to_mesh_element(context, active)

        # finish if the cursor has been set
        if is_cursor_set:
            return {'FINISHED'}

        # fall back for cases not covered above
        bpy.ops.view3d.snap_cursor_to_selected()

        return {'FINISHED'}

    def cursor_to_mesh_element(self, context, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        if context.scene.tool_settings.mesh_select_mode[0]:
            elements = [v for v in bm.verts if v.select]

        elif context.scene.tool_settings.mesh_select_mode[1]:
            elements = [e for e in bm.edges if e.select]

        elif context.scene.tool_settings.mesh_select_mode[2]:
            elements = [f for f in bm.faces if f.select]

        if len(elements) == 1:

            element = elements[0]
            mx = active.matrix_world

            if isinstance(element, bmesh.types.BMVert):
                origin = mx @ element.co
                normal = mx.to_3x3() @ element.normal
                rmx = create_rotation_matrix_from_normal(active, normal)

            elif isinstance(element, bmesh.types.BMEdge):
                origin = mx @ get_center_between_verts(*element.verts)
                rmx = create_rotation_matrix_from_edge(active, element)

            elif isinstance(element, bmesh.types.BMFace):
                origin = mx @ element.calc_center_median()
                normal = mx.to_3x3() @ element.normal
                rmx = create_rotation_matrix_from_normal(active, normal)

                # TODO: add switch to take face shape into account:construct tangent from face normal and longest edge, instead of face normal nad object's up axis

            # create quat from rmx
            quat = rmx.to_quaternion()

            set_cursor(origin, quat)

            return True
        return False

    def cursor_to_active_object(self, active):
        mx = active.matrix_world
        origin, quat, _ = mx.decompose()

        set_cursor(origin, quat)
