import bpy
import bmesh
from .. utils.mesh import unhide_deselect, join
from .. utils.object import flatten, add_facemap, add_vgroup

from time import time


class MeshCut(bpy.types.Operator):
    bl_idname = "machin3.mesh_cut"
    bl_label = "MACHIN3: Mesh Cut"
    bl_description = "Knife Intersect a mesh, using another object.\nALT: flatten target object's modifier stack\nSHIFT: Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) == 2 and context.active_object and context.active_object in context.selected_objects

    def invoke(self, context, event):

        start = time()


        target = context.active_object
        cutter = [obj for obj in context.selected_objects if obj != target][0]

        # unhide both
        unhide_deselect(target.data)
        unhide_deselect(cutter.data)

        # get depsgraph
        dg = context.evaluated_depsgraph_get()

        # flatten the cutter
        flatten(cutter, dg)

        # flatten the target
        if event.alt:
            flatten(target, dg)

        # clear cutter materials
        cutter.data.materials.clear()

        # join target and cutter
        join(target, [cutter], select=[1])

        # knife intersect
        bpy.ops.object.mode_set(mode='EDIT')
        if event.shift:
            bpy.ops.mesh.intersect(separate_mode='ALL')
        else:
            bpy.ops.mesh.intersect(separate_mode='CUT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # remove cutter
        bm = bmesh.new()
        bm.from_mesh(target.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        i = bm.faces.layers.int.verify()

        cuuter_faces = [f for f in bm.faces if f[i] > 0]
        bmesh.ops.delete(bm, geom=cuuter_faces, context='FACES')

        # mark seams
        if event.shift:
            non_manifold = [e for e in bm.edges if not e.is_manifold]

            for e in non_manifold:
                e.seam = True

            bmesh.ops.remove_doubles(bm, verts=list({v for e in non_manifold for v in e.verts}), dist=0.0001)

        bm.to_mesh(target.data)
        bm.clear()

        print(time() - start)

        return {'FINISHED'}
