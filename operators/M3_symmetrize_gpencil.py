import bpy
from bpy.props import EnumProperty, BoolProperty
from .. import M3utils as m3


mirroraxis = [("X", "X", ""),
              ("Y", "Y", ""),
              ("Z", "Z", "")]

deleteside = [("NEG", "Negative", ""),
              ("POS", "Positive", "")]


class SymmetrizeGPencil(bpy.types.Operator):
    bl_idname = "machin3.symmetrize_gpencil"
    bl_label = "MACHIN3: Symmetrize GPencil"
    bl_options = {'REGISTER', 'UNDO'}

    mirror = EnumProperty(name="Mirror Axis", items=mirroraxis, default="X")
    delete = BoolProperty(name="Delete", default=True)
    deleteside = EnumProperty(name="Delete Side", items=deleteside, default="NEG")

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        row = column.row(align=True)
        row.prop(self, "mirror", expand=True)

        row = column.row(align=True)
        row.prop(self, "delete")
        row.prop(self, "deleteside", expand=True)

    def execute(self, context):
        gtoggled = False
        if context.gpencil_data:
            if not context.gpencil_data.use_stroke_edit_mode:
                bpy.ops.gpencil.editmode_toggle()
                gtoggled = True
        else:  # no grease pencil in the scene
            return {'FINISHED'}

        cursorloc = bpy.context.scene.cursor_location
        gplayer = bpy.context.active_gpencil_layer

        if self.delete:
            bpy.ops.gpencil.select_all(action='DESELECT')

            for stroke in gplayer.active_frame.strokes:
                for point in stroke.points:
                    if self.mirror == "X":
                        if self.deleteside == "NEG":
                            if point.co[0] < (cursorloc[0]):
                                point.select = True
                        else:
                            if point.co[0] > (cursorloc[0]):
                                point.select = True
                    elif self.mirror == "Y":
                        if self.deleteside == "NEG":
                            if point.co[1] < (cursorloc[1]):
                                point.select = True
                        else:
                            if point.co[1] > (cursorloc[1]):
                                point.select = True
                    elif self.mirror == "Z":
                        if self.deleteside == "NEG":
                            if point.co[2] < (cursorloc[2]):
                                point.select = True
                        else:
                            if point.co[1] > (cursorloc[1]):
                                point.select = True
            try:
                bpy.ops.gpencil.delete(type='POINTS')
            except:  # no grease pencil layer or empty layer
                return {'FINISHED'}

        pivot = m3.change_pivot("CURSOR")
        bpy.ops.gpencil.select_all(action='SELECT')

        try:
            bpy.ops.gpencil.copy()
        except:
            return {'FINISHED'}  # nothing selected (because it was all neg deleted)

        if self.mirror == "X":
            bpy.ops.transform.mirror(constraint_axis=(True, False, False))
        elif self.mirror == "Y":
            bpy.ops.transform.mirror(constraint_axis=(False, True, False))
        elif self.mirror == "Z":
            bpy.ops.transform.mirror(constraint_axis=(False, False, True))

        bpy.ops.gpencil.paste()
        bpy.ops.gpencil.select_all(action='DESELECT')

        pivot = m3.change_pivot(pivot)

        if gtoggled:
            bpy.ops.gpencil.editmode_toggle()

        return {'FINISHED'}
