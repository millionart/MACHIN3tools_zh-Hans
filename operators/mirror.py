import bpy
from bpy.props import BoolProperty
from .. utils.registration import get_addon
from .. utils import MACHIN3 as m3


class Mirror(bpy.types.Operator):
    bl_idname = "machin3.mirror"
    bl_label = "MACHIN3: Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    use_x: BoolProperty(name="X", default=True)
    use_y: BoolProperty(name="Y", default=False)
    use_z: BoolProperty(name="Z", default=False)

    DM_mirror_u: BoolProperty(name="U", default=True)
    DM_mirror_v: BoolProperty(name="V", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "use_x", toggle=True)
        row.prop(self, "use_y", toggle=True)
        row.prop(self, "use_z", toggle=True)

        DMenabled, _, _, _ = get_addon("DECALmachine")
        if DMenabled:
            column.separator()

            column.label(text="DECALmachine - UVs")
            row = column.row(align=True)
            row.prop(self, "DM_mirror_u", toggle=True)
            row.prop(self, "DM_mirror_v", toggle=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        sel = context.selected_objects
        active = context.active_object

        self.mirror(context, active, sel)

        return {'FINISHED'}

    def mirror(self, context, active, sel):
        if len(sel) > 1 and active in sel:
            sel.remove(active)

            for obj in sel:
                if obj.type in ["MESH", "CURVE"]:

                    mirror = obj.modifiers.new(name="Mirror", type="MIRROR")
                    mirror.use_axis = (self.use_x, self.use_y, self.use_z)
                    mirror.mirror_object = active

                    DMenabled, _, _, _ = get_addon("DECALmachine")

                    if DMenabled:
                        if obj.DM.isdecal:
                            mirror.use_mirror_u = self.DM_mirror_u
                            mirror.use_mirror_v = self.DM_mirror_v

                            nrmtransfer = obj.modifiers.get("NormalTransfer")

                            if nrmtransfer:
                                context.view_layer.objects.active = obj
                                while obj.modifiers.keys().index(nrmtransfer.name) < obj.modifiers.keys().index(mirror.name):
                                    bpy.ops.object.modifier_move_up(modifier=mirror.name)

            context.view_layer.objects.active = active
