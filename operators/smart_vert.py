import bpy
import bmesh
from bpy.props import EnumProperty, BoolProperty
from .. utils import MACHIN3 as m3
from .. utils.graph import get_shortest_path


# TODO. the slide tool is a great candidate for testing custom drawing in 2.8
# TODO: i's also great candidate for testing an improved modal bmesh approach


modeitems = [("MERGE", "Merge", ""),
             ("CONNECT", "Connect Paths", "")]


mergetypeitems = [("LAST", "Last", ""),
                  ("CENTER", "Center", ""),
                  ("PATHS", "Paths", "")]

pathtypeitems = [("TOPO", "Topo", ""),
                 ("LENGTH", "Length", "")]


class SmartVert(bpy.types.Operator):
    bl_idname = "machin3.smart_vert"
    bl_label = "MACHIN3: Smart Vert"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Mode", items=modeitems, default="MERGE")
    mergetype: EnumProperty(name="Merge Type", items=mergetypeitems, default="LAST")
    pathtype: EnumProperty(name="Path Type", items=pathtypeitems, default="TOPO")

    slideoverride: BoolProperty(name="Slide Override", default=False)

    # hidden
    wrongselection = False

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        if not self.slideoverride:
            row = column.split(factor=0.3)
            row.label(text="Mode")
            r = row.row()
            r.prop(self, "mode", expand=True)

            if self.mode == "MERGE":
                row = column.split(factor=0.3)
                row.label(text="Merge")
                r = row.row()
                r.prop(self, "mergetype", expand=True)

            if self.mode == "CONNECT" or (self.mode == "MERGE" and self.mergetype == "PATHS"):
                if self.wrongselection:
                    column.label(text="You need to select exactly 4 vertices for paths.", icon="INFO")

                else:
                    row = column.split(factor=0.3)
                    row.label(text="Shortest Path")
                    r = row.row()
                    r.prop(self, "pathtype", expand=True)

    @classmethod
    def poll(cls, context):
        return m3.get_mode() == "VERT"

    def execute(self, context):
        self.smart_vert(context)

        return {'FINISHED'}

    def smart_vert(self, context):
        active = context.active_object

        # SLIDE EXTEND

        if self.slideoverride:
            self.slide(context)

        else:
            selverts = m3.get_selection("VERT")


            # MERGE

            if self.mode == "MERGE":

                if self.mergetype == "LAST":
                    if len(selverts) >= 2:
                        if self.has_valid_select_history(active, lazy=True):
                            bpy.ops.mesh.merge(type='LAST')

                elif self.mergetype == "CENTER":
                    if len(selverts) >= 2:
                        bpy.ops.mesh.merge(type='CENTER')

                elif self.mergetype == "PATHS":
                    self.wrongselection = False

                    if len(selverts) == 4:
                        bm, history = self.has_valid_select_history(active)

                        if history:
                            topo = True if self.pathtype == "TOPO" else False
                            bm, path1, path2 = self.get_paths(bm, history, topo)

                            self.weld(active, bm, path1, path2)
                            return

                    self.wrongselection = True


            # CONNECT

            elif self.mode == "CONNECT":
                self.wrongselection = False

                if len(selverts) == 4:
                    bm, history = self.has_valid_select_history(active)

                    if history:
                        topo = True if self.pathtype == "TOPO" else False
                        bm, path1, path2 = self.get_paths(bm, history, topo)

                        self.connect(active, bm, path1, path2)
                        return

                self.wrongselection = True

    def get_paths(self, bm, history, topo):
        pair1 = history[0:2]
        pair2 = history[2:4]
        pair2.reverse()

        path1 = get_shortest_path(bm, *pair1, topo=topo, select=True)
        path2 = get_shortest_path(bm, *pair2, topo=topo, select=True)

        return bm, path1, path2

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

    def weld(self, active, bm, path1, path2):
        targetmap = {}
        for v1, v2 in zip(path1, path2):
            targetmap[v1] = v2

        bmesh.ops.weld_verts(bm, targetmap=targetmap)

        bmesh.update_edit_mesh(active.data)

    def connect(self, active, bm, path1, path2):
        for verts in zip(path1, path2):
            if not bm.edges.get(verts):
                bmesh.ops.connect_vert_pair(bm, verts=verts)

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

            # remember previous transform orientatinon
            old_orientation = context.scene.transform_orientation_slots[0].type

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
            context.scene.transform_orientation_slots[0].type = old_orientation
