import bpy
from bpy.props import BoolProperty, EnumProperty
from .. import M3utils as m3

modes = [("OPT_1", "Negative Sides", ""),
         ("OPT_2", "Centers", ""),
         ("OPT_3", "Positive Sides", "")]

relatives = [("OPT_1", "Scene Origin", ""),
             ("OPT_2", "3D Cursor", ""),
             ("OPT_3", "Selection", ""),
             ("OPT_4", "Active", "")]


class Align(bpy.types.Operator):
    bl_idname = "machin3.align"
    bl_label = "MACHIN3: Align"
    bl_options = {'REGISTER', 'UNDO'}

    parent = BoolProperty(name="Parent")
    autoskin = BoolProperty(name="Auto Skin")

    highquality = BoolProperty(name="High Quality", default=True)

    alignmode = EnumProperty(name="Align Mode", items=modes, default="OPT_2")
    relativeto = EnumProperty(name="Relative To Mode", items=relatives, default="OPT_4")

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        activetype = m3.get_active().type

        if activetype == "ARMATURE":
            column.prop(self, "parent")
            column.prop(self, "autoskin")
        else:
            column.prop(self, "highquality")
            column.prop(self, "alignmode")
            column.prop(self, "relativeto")

            row = column.row(align=True)
            row.prop(self, "axisx", toggle=True)
            row.prop(self, "axisy", toggle=True)
            row.prop(self, "axisz", toggle=True)

    def execute(self, context):
        sel = m3.selected_objects()
        active = m3.get_active()
        sel.remove(active)

        if active.type == "ARMATURE":
            self.align_to_bone(active, bpy.context.active_bone, sel)
        else:
            self.align(active, sel)

        return {'FINISHED'}

    def align_to_bone(self, active, activebone, selection):
        for obj in selection:
            print("Aligning '%s' to Bone '%s' of Armature '%s'." % (obj.name, activebone.name, active.name))

            if self.parent:
                if obj.parent:
                    m3.make_active(obj)
                    bpy.ops.object.parent_clear(type='CLEAR')
                    m3.make_active(active)

            obj.matrix_local = activebone.matrix_local
            obj.data.update()

            if self.parent:
                    bpy.ops.object.parent_set(type='BONE')

            if self.autoskin:
                armature = obj.modifiers.get("Armature")
                if not armature:
                    armature = obj.modifiers.new(name="Armature", type="ARMATURE")
                else:
                    print("Using existing Armature modifier.")

                armature.object = active

                bonevgroup = obj.vertex_groups.get(activebone.name)
                if not bonevgroup:
                    bonevgroup = obj.vertex_groups.new(name=activebone.name)
                else:
                    print("Using existing Vertex Group '%s'." % (activebone.name))

                vids = [vid.index for vid in obj.data.vertices]
                bonevgroup.add(vids, 1, "REPLACE")

    def align(self, active, selection):
        axisset = set()

        if self.axisx:
            axisset.add("X")
        if self.axisy:
            axisset.add("Y")
        if self.axisz:
            axisset.add("Z")

        bpy.ops.object.align(bb_quality=self.highquality, align_mode=self.alignmode, relative_to=self.relativeto, align_axis=axisset)
