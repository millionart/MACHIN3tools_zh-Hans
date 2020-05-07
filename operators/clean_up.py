import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty
import bmesh
import math


selecttypeitems = [("NON-MANIFOLD", "非流形", ""),
                   ("TRIS", "三角面", ""),
                   ("NGONS", "盎司", "")]


class CleanUp(bpy.types.Operator):
    bl_idname = "machin3.clean_up"
    bl_label = "MACHIN3: 清理"
    bl_options = {'REGISTER', 'UNDO'}

    remove_doubles: BoolProperty(name="移除重复", default=True)
    dissolve_degenerate: BoolProperty(name="溶并无用", default=True)
    distance: FloatProperty(name="合并距离", default=0.0001, min=0, step=0.01, precision=4)

    recalc_normals: BoolProperty(name="重新计算法线", default=True)
    flip_normals: BoolProperty(name="翻转法线", default=False)

    delete_loose: BoolProperty(name="删除松散", default=True)
    delete_loose_verts: BoolProperty(name="删除松散 点", default=True)
    delete_loose_edges: BoolProperty(name="删除松散 线", default=True)
    delete_loose_faces: BoolProperty(name="删除松散 面", default=False)

    dissolve_2_edged: BoolProperty(name="溶并线段上的点", default=True)
    angle_threshold: FloatProperty(name="角度阈值", default=179, min=0, max=180)

    select: BoolProperty(name="选择", default=True)
    select_type: EnumProperty(name="选择", items=selecttypeitems, default="NON-MANIFOLD")

    view_selected: BoolProperty(name="查看选中项", default=False)

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        col = box.column()

        row = col.row()
        row.prop(self, "remove_doubles", text="重复")
        row.prop(self, "dissolve_degenerate", text="无用")
        r = row.row()
        r.active = any([self.remove_doubles, self.dissolve_degenerate])
        r.prop(self, "distance", text="")

        row = col.split(factor=0.33)
        row.prop(self, "delete_loose", text="松散")
        r = row.row(align=True)
        r.active = self.delete_loose
        r.prop(self, "delete_loose_verts", text="点", toggle=True)
        r.prop(self, "delete_loose_edges", text="线", toggle=True)
        r.prop(self, "delete_loose_faces", text="面", toggle=True)

        row = col.row()
        row.prop(self, "dissolve_2_edged", text="线段上的点")
        r = row.row()
        r.active = self.dissolve_2_edged
        r.prop(self, "angle_threshold", text="角度")

        row = col.row()
        row.prop(self, "recalc_normals")
        r = row.row()
        r.active = self.recalc_normals
        r.prop(self, "flip_normals", text="Flip", toggle=True)

        box = layout.box()
        col = box.column()

        row = col.row()
        row.prop(self, "select")
        r = row.row()
        r.active = self.select
        r.prop(self, "view_selected")

        row = col.row()
        row.active = self.select
        row.prop(self, "select_type", expand=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def execute(self, context):
        active = context.active_object

        bm = self.clean_up(active)

        if self.select:
            self.select_geometry(bm)

        bmesh.update_edit_mesh(active.data)

        if self.select and self.view_selected:
            bpy.ops.view3d.view_selected(use_all_regions=False)

        return {'FINISHED'}

    def clean_up(self, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        if self.remove_doubles:
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=self.distance)

        if self.dissolve_degenerate:
            bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=self.distance)

        if self.delete_loose:
            self.delete_loose_geometry(bm)

        if self.dissolve_2_edged:
            self.dissolve_2_edged_verts(bm)

        if self.recalc_normals:
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

            if self.flip_normals:
                for f in bm.faces:
                    f.normal_flip()

        return bm

    def delete_loose_geometry(self, bm):
        if self.delete_loose_verts:
            loose_verts = [v for v in bm.verts if not v.link_edges]
            bmesh.ops.delete(bm, geom=loose_verts, context="VERTS")

        if self.delete_loose_edges:
            loose_edges = [e for e in bm.edges if not e.link_faces]
            bmesh.ops.delete(bm, geom=loose_edges, context="EDGES")

        if self.delete_loose_faces:
            loose_faces = [f for f in bm.faces if all([not e.is_manifold for e in f.edges])]
            bmesh.ops.delete(bm, geom=loose_faces, context="FACES")

    def dissolve_2_edged_verts(self, bm):
        all_2_edged_verts = [v for v in bm.verts if len(v.link_edges) == 2]

        straight_edged = []

        for v in all_2_edged_verts:
            e1 = v.link_edges[0]
            e2 = v.link_edges[1]

            vector1 = e1.other_vert(v).co - v.co
            vector2 = e2.other_vert(v).co - v.co

            angle = math.degrees(vector1.angle(vector2))

            if self.angle_threshold + 1 <= angle <= 181:
                straight_edged.append(v)

        bmesh.ops.dissolve_verts(bm, verts=straight_edged)

    def select_geometry(self, bm):
        for f in bm.faces:
            f.select = False

        bm.select_flush(False)

        if self.select_type == "NON-MANIFOLD":
            edges = [e for e in bm.edges if not e.is_manifold]

            for e in edges:
                e.select = True

        elif self.select_type == "TRIS":
            faces = [f for f in bm.faces if len(f.verts) == 3]

            for f in faces:
                f.select = True

        elif self.select_type == "NGONS":
            faces = [f for f in bm.faces if len(f.verts) > 4]

            for f in faces:
                f.select = True
