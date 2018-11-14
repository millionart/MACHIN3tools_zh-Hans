import bpy
from bpy.props import BoolProperty
from .. import M3utils as m3


lockchoice = [("LOCK", "Lock", ""),
              ("UNLOCK", "Unlock", "")]


class LockItAll(bpy.types.Operator):
    bl_idname = "machin3.lock_it_all"
    bl_label = "MACHIN3: Lock It All"
    bl_options = {'REGISTER', 'UNDO'}

    location = BoolProperty(name="Location", default=True)
    rotation = BoolProperty(name="Rotation", default=True)
    scale = BoolProperty(name="Scale", default=True)

    lockorunlock = bpy.props.EnumProperty(name="Lock or Unlock", items=lockchoice, default="LOCK")

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "lockorunlock", expand=True)

        column.separator()

        column.prop(self, "location", toggle=True)
        column.prop(self, "rotation", toggle=True)
        column.prop(self, "scale", toggle=True)

    def execute(self, context):
        selection = m3.selected_objects()

        if self.lockorunlock == "LOCK":
            lock = True
        else:
            lock = False

        for obj in selection:
            if self.location:
                for i in range(len(obj.lock_location)):
                    obj.lock_location[i] = lock
                    print("Locked '%s's location[%d]." % (obj.name, i))
                if any([self.rotation, self.scale]):
                    print("---")
            if self.rotation:
                for i in range(len(obj.lock_rotation)):
                    obj.lock_rotation[i] = lock
                    print("Locked '%s's rotation[%d]." % (obj.name, i))
                if self.scale:
                    print("---")
            if self.scale:
                for i in range(len(obj.lock_scale)):
                    obj.lock_scale[i] = lock
                    print("Locked '%s's scale[%d]." % (obj.name, i))
            if any([self.location, self.rotation, self.scale]):
                print("_" * 40)

        return {'FINISHED'}
