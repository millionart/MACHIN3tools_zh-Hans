import bpy
from bpy.props import EnumProperty
from .. import M3utils as m3

hidechoice = [("HIDE", "Hide", ""),
              ("UNHIDE", "Unhide", "")]


class HideMeshes(bpy.types.Operator):
    bl_idname = "machin3.hide_meshes"
    bl_label = "MACHIN3: Hide Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    hideorunhide = EnumProperty(name="Hide or Unhide", items=hidechoice, default="HIDE")

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "hideorunhide", expand=True)

    def execute(self, context):
        selection = m3.selected_objects()
        active = m3.get_active()

        if self.hideorunhide == "HIDE":
            hide = True
        else:
            hide = False

        for obj in selection:
            if obj.type == "MESH":
                m3.make_active(obj)
                m3.set_mode("EDIT")
                if hide:
                    m3.select_all("MESH")
                    bpy.ops.mesh.hide(unselected=False)
                    print("'%s's geometry hidden." % (obj.name))
                else:
                    m3.unhide_all("MESH")
                    print("'%s's geometry unhidden." % (obj.name))
                bpy.ops.object.mode_set(mode='OBJECT')

        m3.make_active(active)
        return {'FINISHED'}
