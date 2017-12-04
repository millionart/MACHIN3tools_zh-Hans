import bpy
from bpy.props import BoolProperty, EnumProperty
from .. import M3utils as m3


joinorconnectchoice = [("JOIN", "Join", ""),
                       ("CONNECT", "Connect", "")]


class QuickJoinCenter(bpy.types.Operator):
    bl_idname = "machin3.quick_join_center"
    bl_label = "MACHIN3: Quick Join (Center)"
    bl_options = {'REGISTER', 'UNDO'}

    backtrace = BoolProperty(name="Backtrace Selection", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "backtrace")

    def execute(self, context):
        history = m3.get_selection_history()

        if len(history) > 3:
            quick_join("CENTER", history, self.backtrace, "JOIN")
        else:
            bpy.ops.mesh.merge(type='CENTER')

        return {'FINISHED'}


class QuickJoinLast(bpy.types.Operator):
    bl_idname = "machin3.quick_join_last"
    bl_label = "MACHIN3: Quick Join (Last)"
    bl_options = {'REGISTER', 'UNDO'}

    backtrace = BoolProperty(name="Backtrace Selection", default=True)
    joinorconnect = EnumProperty(name="Join or Connect", items=joinorconnectchoice, default="JOIN")

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "joinorconnect", expand=True)

        column.prop(self, "backtrace")

    def execute(self, context):

        history = m3.get_selection_history()
        if len(history) > 3:
            quick_join("LAST", history, self.backtrace, self.joinorconnect)
        else:
            bpy.ops.mesh.merge(type='LAST')

        return {'FINISHED'}


def quick_join(string, selection, backtrace, joinorconnect):
    mergeswitched = False
    pivotswitched = False
    aborted = False
    if bpy.context.scene.tool_settings.use_mesh_automerge:
        print("automerge is on, turning it off.")
        bpy.context.scene.tool_settings.use_mesh_automerge = False
        mergeswitched = True
    if bpy.context.space_data.pivot_point != "MEDIAN_POINT":
        pivot = bpy.context.space_data.pivot_point
        print('Pivot is "%s", changing it to "MEDIAN_POINT".' % (pivot))
        bpy.context.space_data.pivot_point = "MEDIAN_POINT"
        pivotswitched = True

    split = split_selection(selection)
    try:
        path1, path2 = pathify(split)
    except:
        print(m3.red("Aborting quick-join."))
        aborted = True

    if not aborted:
        try:
            join(string, path1, path2, backtrace, joinorconnect)
        except:
            print(m3.red("Results will be unpredictable."))

    if mergeswitched:
        print("Automerge has been switched off, turning it back on again.")
        bpy.context.scene.tool_settings.use_mesh_automerge = True
    if pivotswitched:
        print('Pivot has been changed, setting it back to "%s".' % (pivot))
        bpy.context.space_data.pivot_point = pivot


def join(string, vertlist1, vertlist2, backtrace, joinorconnect):  # joining by moving/scaling, as vertids would be changing when using the actual merge operator
    bpy.context.scene.tool_settings.use_mesh_automerge = False
    mesh = bpy.context.object.data

    # reverse the second path to allow for a backtracing selection
    if backtrace:
        vertlist2.reverse()

    for vert in vertlist1:
        vert2 = vertlist2[vertlist1.index(vert)]
        m3.unselect_all("MESH")
        m3.set_mode("OBJECT")

        mesh.vertices[vert].select = True
        mesh.vertices[vert2].select = True

        if string == "LAST":
            print("Moving: %d > %d." % (vert, vert2))
            if joinorconnect == "JOIN":
                mesh.vertices[vert].co = mesh.vertices[vert2].co  # JOIN LAST
            m3.set_mode("EDIT")
            if joinorconnect == "CONNECT":
                bpy.ops.mesh.vert_connect()
        elif string == "CENTER":
            m3.set_mode("EDIT")
            print("Moving: %d and %d to median location." % (vert, vert2))
            bpy.ops.transform.resize(value=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    m3.unselect_all("MESH")
    if joinorconnect == "CONNECT":
        m3.set_mode("EDIT")
    elif joinorconnect == "JOIN":
        m3.make_selection("VERT", vertlist1 + vertlist2)
        m3.set_mode("EDIT")

        bpy.ops.mesh.remove_doubles()


def pathify(verttuple):
    if verttuple is not None:
        row1, row2 = verttuple
        print(row1)
        print(row2)

        p1 = m3.ShortestPath(input=row1)
        p2 = m3.ShortestPath(input=row2)
        if len(p1.path) == len(p2.path):
            print(p1.path)
            print(p2.path)
            return p1.path, p2.path
        else:
            print(m3.red("Warning, Vertex paths are not equal in length."))
            return p1.path, p2.path


def split_selection(vertselection):
    if len(vertselection) % 2 == 0:
        split = int(len(vertselection) / 2)
        hist1 = vertselection[:split]
        hist2 = vertselection[split:]
        return hist1, hist2
    else:
        print(m3.red("Selection is not divisable by 2. Select an equal amount of vertices on both sides."))
