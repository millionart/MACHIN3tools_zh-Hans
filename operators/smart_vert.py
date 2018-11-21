import bpy
import bmesh
from bpy.props import EnumProperty, BoolProperty
from .. utils import MACHIN3 as m3
from .. utils.graph import get_shortest_path


# TODO. the slide tool is a great candidate for testing custom drawnig in 2.8
# TODO: i's also great candidate for testing an improved modal bmesh approach


mergetypeitems = [("LAST", "Last", ""),
                  ("CENTER", "Center", ""),
                  ("SMART", "Smart", "")]


class SmartVert(bpy.types.Operator):
    bl_idname = "machin3.smart_vert"
    bl_label = "MACHIN3: Smart Vert"
    bl_options = {'REGISTER', 'UNDO'}

    type: EnumProperty(name="Merge Type", items=mergetypeitems, default="LAST")
    slide_override: BoolProperty(name="Slide Override", default=False)

    topo: BoolProperty(name="Topo", default=False)

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

            column.prop(self, "topo")

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
                    # TODO: acually, all you need is an active vert, not an entire  history.
                    if self.has_valid_select_history(active, lazy=True):
                        bpy.ops.mesh.merge(type='LAST')

            elif self.type == "CENTER":
                if len(selverts) >= 2:
                    bpy.ops.mesh.merge(type='CENTER')

            elif self.type == "SMART":
                if len(selverts) == 4:

                    bm, history = self.has_valid_select_history(active)

                    if history:
                        pair1 = history[0:2]
                        pair2 = history[2:4]
                        pair2.reverse()

                        path1 = get_shortest_path(bm, *pair1, topo=self.topo, select=True)
                        path2 = get_shortest_path(bm, *pair2, topo=self.topo, select=True)

                        # merge the verts
                        self.weld(bm, path1, path2)

                        bmesh.update_edit_mesh(active.data)

                    else:
                        self.wrongselection = False
                else:
                    self.wrongselection = False

        return {'FINISHED'}

    def has_valid_select_history(self, active, lazy=False):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        verts = [v for v in bm.verts if v.select]
        history = list(bm.select_history)

        # just check for the prence of any element in the history
        if lazy:
            return history

        if len(verts) == len(history):
            return bm, history
        return None, None

    def weld(self, bm, path1, path2):
        targetmap = {}
        for v1, v2 in zip(path1, path2):
            targetmap[v1] = v2

        bmesh.ops.weld_verts(bm, targetmap=targetmap)

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
