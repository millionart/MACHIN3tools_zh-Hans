import bpy
from bpy.props import BoolProperty, EnumProperty
from .. import M3utils as m3


modes = [("SIMPLE", "Simple", ""),
         ("BBOX", "Bounding Box", "")]

bboxmodes = [("OPT_1", "Negative Sides", ""),
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

    mode = EnumProperty(name="Mode", items=modes, default="BBOX")

    alignmode = EnumProperty(name="Align Mode", items=bboxmodes, default="OPT_2")
    highquality = BoolProperty(name="High Quality", default=True)
    relativeto = EnumProperty(name="Relative To Mode", items=relatives, default="OPT_4")

    axisx = BoolProperty(name="X", default=True)
    axisy = BoolProperty(name="Y", default=True)
    axisz = BoolProperty(name="Z", default=True)

    ignoremirror = BoolProperty(name="Ignore Mirror", default=False)
    rotation = BoolProperty(name="Align Rotation", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        activetype = m3.get_active().type

        if activetype == "ARMATURE":
            column.prop(self, "parent")
            column.prop(self, "autoskin")
        else:
            row = column.row(align=True)
            row.prop(self, "axisx", toggle=True)
            row.prop(self, "axisy", toggle=True)
            row.prop(self, "axisz", toggle=True)

            row = column.row()
            row.prop(self, "mode", expand=True)

            split = column.split()
            split.separator()
            col = split.column()
            col.prop(self, "highquality")

            col.prop(self, "alignmode", text="")
            col.prop(self, "relativeto", text="")

            column.prop(self, "rotation")
            column.prop(self, "ignoremirror")

    def execute(self, context):
        sel = m3.selected_objects()
        active = m3.get_active()
        sel.remove(active)

        if active.type == "ARMATURE":
            self.align_to_bone(active, bpy.context.active_bone, sel)
        else:
            if self.ignoremirror:
                self.toggle_mirror()

            self.align(active, sel)

            if self.ignoremirror:
                self.toggle_mirror()

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

    def toggle_mirror(self):
        for obj in bpy.context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == "MIRROR":
                    mod.show_viewport = not mod.show_viewport

    def align(self, active, selection):
        axisset = set()

        if self.axisx:
            axisset.add("X")
        if self.axisy:
            axisset.add("Y")
        if self.axisz:
            axisset.add("Z")

        # NOTE: doing the rotation first is important for the bbox mode.
        if self.rotation:
            # bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0), axis=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.683013)
            bpy.ops.transform.transform(mode='ALIGN')

        if self.mode == "BBOX":
            bpy.ops.object.align(bb_quality=self.highquality, align_mode=self.alignmode, relative_to=self.relativeto, align_axis=axisset)
        elif self.mode == "SIMPLE":
            for obj in selection:
                if self.axisx:
                    obj.location[0] = active.location[0]
                if self.axisy:
                    obj.location[1] = active.location[1]
                if self.axisz:
                    obj.location[2] = active.location[2]
