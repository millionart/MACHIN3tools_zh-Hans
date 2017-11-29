import bpy
from bpy.props import FloatProperty, EnumProperty
import bmesh
from .. import M3utils as m3


scalemode = [("AVERAGE", "Average", ""),
             ("PRECISE", "Precise", "")]

# NOTE: if selected edges are conntected to each other, results will be not as expected


class EdgeLength(bpy.types.Operator):
    bl_idname = "machin3.edge_length"
    bl_label = "MACHIN3: Edge Length"
    bl_options = {'REGISTER', 'UNDO'}

    scalemode = EnumProperty(name="Scale Mode", items=scalemode, default="AVERAGE")
    edgelength = FloatProperty(name="Precise Edge Length", default=0.1, min=0)

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        row = col.row()
        row.prop(self, "scalemode", expand=True)

        col.prop(self, "edgelength")

    def execute(self, context):
        m3.set_mode("OBJECT")

        active = m3.get_active()

        # get selected edges and their lengths
        edges, edgeids = self.get_edges(active)

        if len(edges) > 0:
            if self.scalemode == "AVERAGE":
                # get everage edge length
                scalelength = sum([e[1] for e in edges]) / len(edges)
                print("average length: %f" % (scalelength))
            elif self.scalemode == "PRECISE":
                scalelength = self.edgelength
                print("precise length: %f" % (scalelength))

            m3.set_mode("EDIT")
            m3.set_mode("EDGE")

            for idx, length in edges:
                m3.unselect_all("MESH")
                if length != scalelength:
                    m3.make_selection("EDGE", [idx])
                    scale = scalelength / length
                    bpy.ops.transform.resize(value=(scale, scale, scale))
                    print("scaled edge '%d' from '%f' to '%f'." % (idx, length, scalelength))
                else:
                    print("left edge '%d' unchanged, already at length '%f'." % (idx, scalelength))

            m3.make_selection("EDGE", edgeids)
        else:
            self.report({'ERROR'}, "Select at least one edge!")

        return {'FINISHED'}

    def get_edges(self, obj):
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        edges = []
        edgeids = []
        for edge in bm.edges:
            if edge.select:
                edges.append((edge.index, edge.calc_length()))
                edgeids.append(edge.index)
        return edges, edgeids
