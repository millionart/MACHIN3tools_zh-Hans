import bpy
from bpy.props import BoolProperty
import bmesh
from mathutils import Vector, Quaternion
from .. utils.math import get_loc_matrix, get_rot_matrix, get_sca_matrix


class Apply(bpy.types.Operator):
    bl_idname = "machin3.apply_transformations"
    bl_label = "MACHIN3: Apply Transformations"
    bl_description = "Apply Transformations while keeping the bevel width as well as the child transformations unchanged."
    bl_options = {'REGISTER', 'UNDO'}

    scale: BoolProperty(name="Scale", default=True)
    rotation: BoolProperty(name="Rotation", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "scale", toggle=True)
        row.prop(self, "rotation", toggle=True)


    def execute(self, context):
        if any([self.rotation, self.scale]):
            parents = [obj for obj in context.selected_objects if not obj.parent]

            for obj in parents:

                # fetch children and their current world mx
                children = [(child, child.matrix_world) for child in bpy.data.objects if child.parent == obj]

                mx = obj.matrix_world
                loc, rot, sca = mx.decompose()

                # apply the current transformations on the mesh level
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                bm.normal_update()
                bm.verts.ensure_lookup_table()

                if self.rotation and self.scale:
                    bmmx = get_rot_matrix(rot) @ get_sca_matrix(sca)
                elif self.rotation:
                    bmmx = get_rot_matrix(rot)
                elif self.scale:
                    bmmx = get_sca_matrix(sca)

                bmesh.ops.transform(bm, matrix=bmmx, verts=bm.verts)

                bm.to_mesh(obj.data)
                bm.clear()

                # zero out the transformations on the object level
                if self.rotation and self.scale:
                    applymx = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(Vector.Fill(3, 1))
                elif self.rotation:
                    applymx = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(sca)
                elif self.scale:
                    applymx = get_loc_matrix(loc) @ get_rot_matrix(rot) @ get_sca_matrix(Vector.Fill(3, 1))

                obj.matrix_world = applymx


                # adjust the bevel width values accordingly
                if self.scale:
                    mods = [mod for mod in obj.modifiers if mod.type == "BEVEL"]

                    for mod in mods:
                        vwidth = get_sca_matrix(sca) @ Vector((0, 0, mod.width))
                        mod.width = vwidth[2]


                # reset the children to their original state again
                for obj, mxw in children:
                    obj.matrix_world = mxw

        return {'FINISHED'}
