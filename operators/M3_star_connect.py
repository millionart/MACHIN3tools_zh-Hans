import bpy
import bmesh
from .. import M3utils as m3


class StarConnect(bpy.types.Operator):
    bl_idname = "machin3.star_connect"
    bl_label = "MACHIN3: Star Connect"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = m3.get_comp_mode()

        if mode == "VERT":
            self.vert_star_connect()
        elif mode == "FACE":
            # print("Face mode!")
            bpy.ops.mesh.inset(thickness=0.5)
            bpy.ops.mesh.merge(type='CENTER')
        else:
            pass

        return {'FINISHED'}

    def vert_star_connect(self):
        mesh = bpy.context.object.data

        # we need to switch from Edit mode to Object mode so the selection gets updated
        m3.set_mode("OBJECT")
        selected = [v.index for v in mesh.vertices if v.select]

        # bmesh needs to be in  edit mode
        m3.set_mode("EDIT")

        try:  # here we try to get get the star vert from the selection history
            bm = bmesh.from_edit_mesh(mesh)
            vertlist = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
            lastvert = vertlist[-1]
        except:  # alternatively you can also select everything with the box or circle, if the star vert has been created after the streak verts, which is usually the case
            lastvert = selected[-1]

        # remove star vert from selection
        selected.remove(lastvert)

        print("Selected verts: %s" % (selected))
        print("Last vert(star): %d" % (lastvert))

        for v in selected:
            m3.unselect_all("MESH")

            # the vertex selection needs to happen in object mode
            m3.set_mode("OBJECT")

            mesh.vertices[v].select = True
            mesh.vertices[lastvert].select = True
            print("Connecting: %d - %d" % (v, lastvert))

            # back into edit mode
            m3.set_mode("EDIT")

            # connect the vert pair
            bpy.ops.mesh.vert_connect_path()
