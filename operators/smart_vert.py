import bpy
import bmesh
from bpy.props import EnumProperty, BoolProperty
from .. utils import MACHIN3 as m3



# TODO. the slide tool is a great candidate for testing custom drawnig in 2.8
# TODO: i's also great candidate for testing an improved modal bmesh approach
# TODO: redo shortest path in bmesh


mergetypeitems = [("LAST", "Last", ""),
                  ("CENTER", "Center", ""),
                  ("SMART", "Smart", "")]


class SmartVert(bpy.types.Operator):
    bl_idname = "machin3.smart_vert"
    bl_label = "MACHIN3: Smart Vert"
    bl_options = {'REGISTER', 'UNDO'}

    type: EnumProperty(name="Merge Type", items=mergetypeitems, default="LAST")
    slide_override: BoolProperty(name="Slide Override", default=False)

    # hidden
    wrongsmartselection = False

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.label(text="Merge")
        row.prop(self, "type", expand=True)

        if self.type == "SMART":
            if self.wrongselection:
                row = column.split(factor=0.25)

                row.separator()
                row.label(text="You need to select exactly 4 vertices.", icon="INFO")

        # NOTE: the slide isn't drawn, even if we wanted, likely due to the transform tool invokation


    @classmethod
    def poll(cls, context):
        return m3.get_mode() == "VERT"


    def execute(self, context):
        active = context.active_object

        # SLIDE aka slide extend aka invisible slide

        if self.slide_override:
            self.slide(context)


        # MERGE

        else:
            selverts = m3.get_selection("VERT")

            if self.type == "LAST":
                if len(selverts) >= 2:
                    if self.has_valid_select_history(active):
                        bpy.ops.mesh.merge(type='LAST')

            elif self.type == "CENTER":
                if len(selverts) >= 2:
                    bpy.ops.mesh.merge(type='CENTER')

            elif self.type == "SMART":
                if len(selverts) == 4:
                    if self.has_valid_select_history(active):
                        self.wrongselection = False

                        # get path starting and end vert ids
                        # also prepare the selection history for the shortest path op
                        path1, path2 = self.get_path_ids(active)

                        # select the shortest path 1
                        bpy.ops.mesh.shortest_path_select()

                        # get full path1 ids
                        path1 = self.get_full_path(active, path1[0], path1[1], deselect=True)

                        # select the shortest path 2
                        self.select_shortest_path_2(active, path2)

                        # get full path2 ids
                        path2 = self.get_full_path(active, path2[1], path2[0])

                        # merge the verts
                        self.weld(active, path1, path2)

                else:
                    self.wrongselection = True

        return {'FINISHED'}

    def has_valid_select_history(self, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]
        history = list(bm.select_history)

        return len(verts) == len(history)

    def get_path_ids(self, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        vertlist = [v for v in bm.select_history if isinstance(v, bmesh.types.BMVert)]

        for v in vertlist[2:]:
            bm.select_history.discard(v)
            v.select = False

        bmesh.update_edit_mesh(active.data)

        return [v.index for v in vertlist[:2]], [v.index for v in vertlist[2:]]

    def select_shortest_path_2(self, active, path2):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        bm.select_history.clear()

        # change selection history, which is what te shortest path op uses
        for vid in path2:
            v = bm.verts[vid]
            bm.select_history.add(v)
            v.select = True

        bm.select_history.validate()

        bmesh.update_edit_mesh(active.data)

        bpy.ops.mesh.shortest_path_select()

    def get_full_path(self, active, v1, v2, deselect=False):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        v_start = bm.verts[v1]
        v_end = bm.verts[v2]
        path = [v_start]

        verts = [v for v in bm.verts if v.select]

        # if a path only consists of 2 verts, the shortest path op will deselect both and the algo below will fail/loop endlessly
        if len(verts) == 0:
            path.append(v_end)

        else:
            v = path[-1]
            while v != v_end:
                for e in v.link_edges:
                    other_v = e.other_vert(v)
                    if other_v in verts and other_v not in path:
                        path.append(other_v)
                        v = other_v

        # interestingly, the selection state will update, even though the bm is not pushed back???
        if deselect:
            for v in path:
                v.select_set(False)

        return [v.index for v in path]

    def weld(self, active, path1, path2):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        targetmap = {}
        for idx1, idx2 in zip(path1, path2):
            v1 = bm.verts[idx1]
            v2 = bm.verts[idx2]

            targetmap[v1] = v2

        bmesh.ops.weld_verts(bm, targetmap=targetmap)

        bmesh.update_edit_mesh(active.data)

    def slide(self, context):
        tool_settings = context.scene.tool_settings

        # turn snapping off
        if tool_settings.use_snap:
            tool_settings.use_snap = False

        active = context.active_object

        # find remove vert to establish the direction
        bm = bmesh.from_edit_mesh(active.data)
        bm.verts.ensure_lookup_table()

        history = list(bm.select_history)

        if history and len(history) == 2:
            v_remote = history[1].index

            # remember previosu transform orientatino
            old_orientation = context.scene.transform_orientation

            # establish direction by creation new transform orientation based on 2 selected vertices
            bpy.ops.transform.create_orientation(name="SlideExtend", use=True, overwrite=True)

            # deselect the remote vert, so we can move only the active
            bm = bmesh.from_edit_mesh(active.data)
            bm.verts.ensure_lookup_table()

            bm.verts[v_remote].select = False
            bm.select_flush(False)

            bmesh.update_edit_mesh(active.data)

            # initiate transformation
            bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_orientation='SlideExtend', constraint_axis=(False, True, False), release_confirm=True)

            # ugly, delete the transform orientation
            bpy.ops.transform.delete_orientation()

            # change the orientation back to what is was before
            context.scene.transform_orientation = old_orientation
