import bpy
from .. import M3utils as m3


class MergeDown(bpy.types.Operator):
    bl_idname = "machin3.merge_down"
    bl_label = "MACHIN3: Merge Down"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = m3.selected_objects()
        active = m3.get_active()

        for obj in selection:
            m3.make_active(obj)

            for mod in obj.modifiers:
                try:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                    print("Applied '%s's '%s' modifier" % (obj.name, mod.name))
                except:
                    print(m3.red("Failed to apply '%s's '%s' modifier") % (obj.name, mod.name))
        m3.make_active(active)
        return {'FINISHED'}
