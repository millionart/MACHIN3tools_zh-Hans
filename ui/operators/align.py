import bpy
from bpy.props import EnumProperty, BoolProperty
import bmesh
from mathutils import Vector, Matrix, geometry
from ... utils.math import get_center_between_verts, create_rotation_difference_matrix_from_quat, get_loc_matrix
from ... items import axis_items, align_type_items, align_axis_mapping_dict


class AlignEditMesh(bpy.types.Operator):
    bl_idname = "machin3.align_editmesh"
    bl_label = "MACHIN3: Align (Edit Mesh)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Default: Local Align\nAlt + Click: Global Align."

    axis: EnumProperty(name="Axis", items=axis_items, default="X")
    type: EnumProperty(name="Type", items=align_type_items, default="MIN")
    local: BoolProperty(name="Local Space", default=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def invoke(self, context, event):
        self.local = not event.alt

        self.align(context, align_axis_mapping_dict[self.axis], self.type, local=self.local)
        return {'FINISHED'}

    def execute(self, context):
        self.align(context, align_axis_mapping_dict[self.axis], self.type, local=self.local)
        return {'FINISHED'}

    def align(self, context, axis, type, local=True):
        active = context.active_object
        mx = active.matrix_world

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]
        axiscoords = [v.co[axis] for v in verts] if local else [(mx @ v.co)[axis] for v in verts]


        # get target value depending on type
        if type == "MIN":
            target = min(axiscoords)

        elif type == "MAX":
            target = max(axiscoords)

        elif type == "ZERO":
            target = 0

        elif type == "AVERAGE":
            target = sum(axiscoords) / len(axiscoords)

        elif type == "CURSOR":
            if local:
                c_world = context.scene.cursor.location
                c_local = mx.inverted() @ c_world
                target = c_local[axis]

            else:
                target = context.scene.cursor.location[axis]


        # set the new coordinates
        for v in verts:
            if local:
                v.co[axis] = target

            else:
                world_co = mx @ v.co
                world_co[axis] = target

                v.co = mx.inverted() @ world_co

        bmesh.update_edit_mesh(active.data)


class AlignObjectToEdge(bpy.types.Operator):
    bl_idname = "machin3.align_object_to_edge"
    bl_label = "MACHIN3: Align Object to Edge"
    bl_description = "Align one or more objects to edge in active object\nALT: Snap objects to edge, in addtion to aligning them"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH':
            active = context.active_object
            sel = [obj for obj in context.selected_objects if obj != active]

            if active and sel:
                for obj in [active] + sel:
                    bm = bmesh.from_edit_mesh(obj.data)

                    if len([e for e in bm.edges if e.select]) != 1:
                        return False
                return True

    def invoke(self, context, event):
        target = context.active_object
        objs = [obj for obj in context.selected_objects if obj != target]

        for obj in objs:

            # get alignment edges
            v_obj, v_target, mid, coords = self.get_vectors_from_alignment_edges(obj, target)

            if v_obj and v_target:
                loc, _, _ = obj.matrix_world.decompose()

                # get rotation matrix
                rmx = create_rotation_difference_matrix_from_quat(v_obj, v_target)

                # bring into the origin, rotate and bring back
                obj.matrix_world = get_loc_matrix(loc) @ rmx @ get_loc_matrix(-loc) @ obj.matrix_world

                # snap the objects together
                if event.alt:
                    # the mid point was returned in local space, and is now brough into world space AFTER the decal was rotated
                    mid = obj.matrix_world @ mid

                    # determine closed point on target edge to decal edge mid ponit
                    co, _ = geometry.intersect_point_line(mid, *coords)

                    # snap the obj to the edge
                    if co:
                        obj.matrix_world = Matrix.Translation(co - mid) @ obj.matrix_world

        return {'FINISHED'}

    def get_vectors_from_alignment_edges(self, obj, target):
        """
        return vectors from both edges, oriented to point in the same direction
        also return the obj edge's midpoint(local space) as well as both vertex coordinates of the target edge (world space)
        """

        bm = bmesh.from_edit_mesh(obj.data)
        edges = [e for e in bm.edges if e.select]

        v_decal = (obj.matrix_world.to_3x3() @ Vector(edges[0].verts[0].co - edges[0].verts[1].co)).normalized() if len(edges) == 1 else None
        mid = get_center_between_verts(*edges[0].verts) if edges else None

        bm = bmesh.from_edit_mesh(target.data)
        edges = [e for e in bm.edges if e.select]

        v_target = (target.matrix_world.to_3x3() @ Vector(edges[0].verts[0].co - edges[0].verts[1].co)).normalized() if len(edges) == 1 else None
        coords = [target.matrix_world @ v.co for v in edges[0].verts] if edges else None

        if v_decal and v_target:

            # align them both the same
            dot = v_decal.dot(v_target)

            if dot < 0:
                v_decal.negate()

            return v_decal, v_target, mid, coords
        return None, None, None, None
