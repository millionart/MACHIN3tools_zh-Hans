import bpy
from .. import M3utils as m3


class FindDisabledMods(bpy.types.Operator):
    bl_idname = "machin3.find_disabled_mods"
    bl_label = "MACHIN3: Find Disabled Mods Modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        m3.clear()

        selection = m3.selected_objects()
        bpy.ops.ed.undo_push(message="testing")

        disabled = []
        for obj in selection:
            m3.make_active(obj)

            for mod in obj.modifiers:
                modname = mod.name
                try:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                except:
                    if obj not in disabled:
                        disabled.append(obj.name)
                        print(obj.name)
                    print(" » " + modname, "is DISABLED!\n")

        # undo applying all those mods, as it's only done to trigger exceptions and find disabled mods
        bpy.ops.ed.undo()

        # for some reason we need to do it through the obj name, we cant directly references the objects(probably as their ids have changed when doing the undo)
        for obj in selection:
            if obj.name in disabled:
                print(obj.name)
            else:
                o = bpy.data.objects[obj.name]
                o.select = False

        return {'FINISHED'}
