import bpy
from bpy.props import BoolProperty
from .. utils import MACHIN3 as m3


class Mirror(bpy.types.Operator):
    bl_idname = "machin3.mirror"
    bl_label = "MACHIN3: Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    use_x: BoolProperty(name="X", default=True)
    use_y: BoolProperty(name="Y", default=False)
    use_z: BoolProperty(name="Z", default=False)

    """
    DM_mirror_u: BoolProperty(name="U", default=True)
    DM_mirror_v: BoolProperty(name="V", default=False)

    DMcustomNormals: BoolProperty(name="re-do custom Normals", default=True)
    DMcopiedNormals: BoolProperty(name="move copied Normals to end of stack", default=True)
    # """

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "use_x", toggle=True)
        row.prop(self, "use_y", toggle=True)
        row.prop(self, "use_z", toggle=True)

        """
        if m3.DM_check():
            column.separator()

            column.label("DECALmachine - UVs")
            row = column.row(align=True)
            row.prop(self, "DMmirrorU", toggle=True)
            row.prop(self, "DMmirrorV", toggle=True)

            column.separator()

            column.label("DECALmachine - custom Normals")
            column.prop(self, "DMcustomNormals")
            column.prop(self, "DMcopiedNormals")
        """

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        sel = m3.selected_objects()
        active = m3.get_active()

        self.mirror(active, sel)

        return {'FINISHED'}

    def mirror(self, active, sel):
        if len(sel) > 1 and active in sel:
            sel.remove(active)

            for obj in sel:
                if obj.type in ["MESH", "CURVE"]:

                    mirror = obj.modifiers.new(name="Mirror", type="MIRROR")

                    mirror.use_x = self.use_x
                    mirror.use_y = self.use_y
                    mirror.use_z = self.use_z

                    mirror.mirror_object = active

                    """

                    if m3.DM_check():
                        # DECALmachine support (u or v mirror for parallax and for info decals!)
                        if obj.DM.isdecal and obj.DM.decaltype in ['SIMPLE', 'SUBSET', 'INFO']:
                            if self.DMmirrorU:
                                mirror.use_mirror_u = True
                            if self.DMmirrorV:
                                mirror.use_mirror_v = True

                        # DECALmachine custom normals, hard custom normals and surface fix support
                        if self.DMcustomNormals:
                            mod = obj.modifiers.get("M3_custom_normals")
                            if mod:
                                src = mod.object

                                srcmirror = src.modifiers.new(name="M3_mirror", type="MIRROR")
                                srcmirror.use_x = self.axisx
                                srcmirror.use_y = self.axisy
                                srcmirror.use_z = self.axisz
                                srcmirror.mirror_object = active

                                m3.make_active(obj)
                                bpy.ops.object.modifier_move_up(modifier=mirror.name)
                                m3.make_active(active)

                            mod = obj.modifiers.get("M3_hard_custom_normals")
                            if mod:
                                src = mod.object

                                srcmirror = src.modifiers.new(name="M3_mirror", type="MIRROR")
                                srcmirror.use_x = self.axisx
                                srcmirror.use_y = self.axisy
                                srcmirror.use_z = self.axisz
                                srcmirror.mirror_object = active

                                m3.make_active(obj)
                                bpy.ops.object.modifier_move_up(modifier=mirror.name)
                                m3.make_active(active)

                            mod = obj.modifiers.get("M3_surface_fix")
                            if mod:
                                src = mod.object

                                srcmirror = src.modifiers.new(name="M3_mirror", type="MIRROR")
                                srcmirror.use_x = self.axisx
                                srcmirror.use_y = self.axisy
                                srcmirror.use_z = self.axisz
                                srcmirror.mirror_object = active

                                m3.make_active(obj)
                                bpy.ops.object.modifier_move_up(modifier=mirror.name)
                                m3.make_active(active)

                        # DECALmachine copied normals support
                        if self.DMcopiedNormals:
                            mod = obj.modifiers.get("M3_copied_normals")
                            if mod:
                                # making obj active for ops
                                m3.make_active(obj)
                                while obj.modifiers[-1].name != "M3_copied_normals":
                                    bpy.ops.object.modifier_move_down(modifier=mod.name)
                                # setting the original active back again
                                m3.make_active(active)
                    # """
