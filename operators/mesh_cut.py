import bpy
from .. utils.mesh import unhide_deselect
from .. utils.object import flatten, add_facemap, add_vgroup


class MeshCut(bpy.types.Operator):
    bl_idname = "machin3.mesh_cut"
    bl_label = "MACHIN3: Mesh Cut"
    bl_description = "Knife Intersect a mesh, using another object.\nALT: flatten target object's modifier stack\nSHIFT: Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) == 2 and context.active_object and context.active_object in context.selected_objects

    def invoke(self, context, event):
        dg = context.evaluated_depsgraph_get()

        target = context.active_object
        cutter = [obj for obj in context.selected_objects if obj != target][0]

        # unhide both
        unhide_deselect(target.data)
        unhide_deselect(cutter.data)

        # flatten the cutter
        flatten(cutter, dg)

        # flatten the target
        if event.alt:
            flatten(target, dg)

        # check for active cutter material
        mat = cutter.active_material

        # clear cutter materials
        if mat:
            cutter.data.materials.clear()

        # initialize face maps
        add_facemap(cutter, name="mesh_cut", ids=[f.index for f in cutter.data.polygons])
        add_facemap(target, name="mesh_cut")

        # join
        bpy.ops.object.join()

        # select cutter mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.face_map_select()

        # knife intersect
        if event.shift:
            bpy.ops.mesh.intersect(separate_mode='ALL')
        else:
            bpy.ops.mesh.intersect(separate_mode='CUT')

        # select cutter mesh and delete it
        bpy.ops.object.face_map_select()
        bpy.ops.mesh.delete(type='FACE')

        # mark non-manifold edges
        if event.shift:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.region_to_loop()

            bpy.ops.mesh.mark_seam(clear=False)
            bpy.ops.mesh.remove_doubles()

        # remove mesh_cut fmap
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.face_map_remove()

        return {'FINISHED'}
