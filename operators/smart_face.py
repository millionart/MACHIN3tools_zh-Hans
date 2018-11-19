import bpy
from bpy.props import FloatProperty, BoolProperty
import bmesh
from .. utils import MACHIN3 as m3


class SmartFace(bpy.types.Operator):
    bl_idname = "machin3.smart_face"
    bl_label = "MACHIN3: Smart Face"
    bl_options = {'REGISTER', 'UNDO'}

    merge: BoolProperty(name="Merge close-by Verts", default=True)
    distance: FloatProperty(name="Merge Distance", default=0.01, min=0, step=0.1, precision=4)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "merge")
        r = row.row()
        r.active = self.merge
        r.prop(self, "distance", text="Distance")

    @classmethod
    def poll(cls, context):
        return m3.get_mode() in ["VERT", "EDGE", "FACE"]

    def execute(self, context):
        mode = m3.get_mode()
        active = m3.get_active()

        if mode in ["VERT", "EDGE"]:
            selverts = m3.get_selection("VERT")

            if selverts:

                # F3

                if 1 <= len(selverts) <= 2:
                    self.f3(active)

                # Blender's face creation

                elif len(selverts) > 2:
                    bpy.ops.mesh.edge_face_add()

        elif mode == "FACE":
            selfaces = m3.get_selection("FACE")

            # DUPLICATE and SEPARATE

            if selfaces:
                bpy.ops.mesh.duplicate()
                bpy.ops.mesh.separate(type='SELECTED')

                m3.set_mode("OBJECT")
                sel = context.selected_objects
                sel.remove(active)
                active.select_set(False)
                m3.make_active(sel[0])
                m3.set_mode("EDIT")

        return {'FINISHED'}

    def f3(self, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]

        if len(verts) == 1:
            v = verts[0]

            faces = v.link_faces
            open_edges = [e for e in v.link_edges if not e.is_manifold]

            if faces and len(open_edges) == 2:

                # calculate the location of the new vert
                e1 = open_edges[0]
                e2 = open_edges[1]

                v1_other = e1.other_vert(v)
                v2_other = e2.other_vert(v)

                v1_dir = v1_other.co - v.co
                v2_dir = v2_other.co - v.co

                # create new vert
                v_new = bm.verts.new()
                v_new.co = v.co + v1_dir + v2_dir

                # create new face
                f = bm.faces.new([v, v2_other, v_new, v1_other])
                f.smooth = any([f.smooth for f in faces])

                # recalc the face normal
                bmesh.ops.recalc_face_normals(bm, faces=[f])

                # TODO: you really should do the remmove dobules here, and then increase the ==4 to >= 4
                # ####: doing that risks removing verts you are refering below however, thereby causing an exception.
                # ####_ what you really need to do is remove doubles only for the new verts against the closest of all others

                # if any of the other two verts has 4 edges, at least one of them non-manifold, select it. first come first serve.
                if any([len(v1_other.link_edges) == 4, len(v2_other.link_edges) == 4]):
                    if len(v1_other.link_edges) == 4 and any([not e.is_manifold for e in v1_other.link_edges]):
                        v.select = False
                        v1_other.select = True
                        v = v1_other

                    elif len(v2_other.link_edges) == 4 and any([not e.is_manifold for e in v2_other.link_edges]):
                        v.select = False
                        v2_other.select = True
                        v = v2_other
                    else:
                        v.select = False
                        bm.select_flush(False)

                    bm.select_flush(False)

                    # for the newly selected vert, check if there is an other vert with 4 edges, select it if so
                    second_vs = [e.other_vert(v) for e in v.link_edges if not e.is_manifold and len(e.other_vert(v).link_edges) == 4]

                    if second_vs:
                        second_v = second_vs[0]
                        second_v.select = True

                        bm.select_flush(True)

                else:
                    v.select = False
                    # v_new.select = True  # it's better to not have anything selected, than select a vert that's only useful in some circumstances

                    bm.select_flush(False)

                # remove dounbles, for new verts close the existing ones
                if self.merge:
                    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=self.distance)


        if len(verts) == 2:
            v1 = verts[0]
            v2 = verts[1]
            e12 = bm.edges.get([v1, v2])

            faces = [f for v in [v1, v2] for f in v.link_faces]

            v1_edges = [e for e in v1.link_edges if e != e12 and not e.is_manifold]
            v2_edges = [e for e in v2.link_edges if e != e12 and not e.is_manifold]

            if v1_edges and v2_edges:
                v1_other = v1_edges[0].other_vert(v1)
                v2_other = v2_edges[0].other_vert(v2)

                # create new face
                if v1_other == v2_other:
                    f = bm.faces.new([v1, v1_other, v2])
                else:
                    f = bm.faces.new([v1, v1_other, v2_other, v2])

                f.smooth = any([f.smooth for f in faces])

                # recalc the face normal
                bmesh.ops.recalc_face_normals(bm, faces=[f])

                v1.select = False
                v2.select = False

                # only select the new verts if they have 4 edges and at least one of them non manifold
                if len(v1_other.link_edges) == 4 and any([not e.is_manifold for e in v1_other.link_edges]):
                    v1_other.select = True

                if len(v2_other.link_edges) == 4 and any([not e.is_manifold for e in v2_other.link_edges]):
                    v2_other.select = True

                bm.select_flush(False)

                # if there is one vert left, check if it has an other vert with 4 edges
                if v1_other.select and not v2_other.select:
                    v1 = v1_other
                    v2 = v2_other

                    second_vs = [e.other_vert(v1) for e in v1.link_edges if not e.is_manifold and e.other_vert(v1) != v2 and len(e.other_vert(v1).link_edges) == 4]
                    if second_vs:
                        second_v = second_vs[0]
                        second_v.select = True

                elif v2_other.select and not v1_other.select:
                    v1 = v1_other
                    v2 = v2_other

                    second_vs = [e.other_vert(v2) for e in v2.link_edges if not e.is_manifold and e.other_vert(v2) != v1 and len(e.other_vert(v2).link_edges) == 4]
                    if second_vs:
                        second_v = second_vs[0]
                        second_v.select = True

                bm.select_flush(True)


        bmesh.update_edit_mesh(active.data)
