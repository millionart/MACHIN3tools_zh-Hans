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

    location = BoolProperty(name="Align Location", default=True)
    rotation = BoolProperty(name="Align Rotation", default=False)

    parent = BoolProperty(name="Parent")
    autoskin = BoolProperty(name="Auto Skin")

    mode = EnumProperty(name="Mode", items=modes, default="SIMPLE")

    locaxisx = BoolProperty(name="X", default=True)
    locaxisy = BoolProperty(name="Y", default=True)
    locaxisz = BoolProperty(name="Z", default=True)

    alignmode = EnumProperty(name="Align Mode", items=bboxmodes, default="OPT_2")
    highquality = BoolProperty(name="High Quality", default=True)
    relativeto = EnumProperty(name="Relative To Mode", items=relatives, default="OPT_4")

    rotaxisx = BoolProperty(name="X", default=True)
    rotaxisy = BoolProperty(name="Y", default=True)
    rotaxisz = BoolProperty(name="Z", default=True)

    ignoremirror = BoolProperty(name="Ignore Mirror Modifier", default=False)

    def draw(self, context):
        layout = self.layout

        activetype = m3.get_active().type

        if activetype == "ARMATURE":
            box = layout.box()
            column = box.column()
            column.prop(self, "parent")
            column.prop(self, "autoskin")
        else:
            box = layout.box()
            column = box.column()
            column.prop(self, "location")

            row = column.row(align=True)
            row.prop(self, "locaxisx", toggle=True)
            row.prop(self, "locaxisy", toggle=True)
            row.prop(self, "locaxisz", toggle=True)

            row = column.row()
            row.prop(self, "mode", expand=True)

            split = column.split()
            split.separator()
            col = split.column()

            col.prop(self, "alignmode", text="")
            col.prop(self, "relativeto", text="")

            col.prop(self, "highquality")
            col.prop(self, "ignoremirror")

            box = layout.box()
            column = box.column()
            column.prop(self, "rotation")

            row = column.row(align=True)
            row.prop(self, "rotaxisx", toggle=True)
            row.prop(self, "rotaxisy", toggle=True)
            row.prop(self, "rotaxisz", toggle=True)

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
        locaxisset = set()

        if self.locaxisx:
            locaxisset.add("X")
        if self.locaxisy:
            locaxisset.add("Y")
        if self.locaxisz:
            locaxisset.add("Z")

        if self.rotation:  # NOTE: doing the rotation first is important for the bbox mode.
            if active.rotation_mode != "XYZ":
                active.rotation_mode = "XYZ"

            for obj in selection:
                if obj.rotation_mode != "XYZ":
                    obj.rotation_mode = "XYZ"

                if self.rotaxisx:
                    obj.rotation_euler[0] = active.rotation_euler[0]
                if self.rotaxisy:
                    obj.rotation_euler[1] = active.rotation_euler[1]
                if self.rotaxisz:
                    obj.rotation_euler[2] = active.rotation_euler[2]

        if self.location:
            if self.mode == "BBOX":
                bpy.ops.object.align(bb_quality=self.highquality, align_mode=self.alignmode, relative_to=self.relativeto, align_axis=locaxisset)
            elif self.mode == "SIMPLE":
                for obj in selection:
                    if self.locaxisx:
                        obj.location[0] = active.location[0]
                    if self.locaxisy:
                        obj.location[1] = active.location[1]
                    if self.locaxisz:
                        obj.location[2] = active.location[2]
