import bpy
from bpy.props import IntProperty, BoolProperty
from .. import M3utils as m3


class SurfaceSnap(bpy.types.Operator):
    bl_idname = "machin3.surface_snap"
    bl_label = "MACHIN3: Surface Snap"
    bl_options = {'REGISTER', 'UNDO'}

    loops = IntProperty(name="Amount of Edge Loops to conform", default=5, min=1, max=10)
    parent = BoolProperty(name="Parent", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "loops")
        column.prop(self, "parent")

    def execute(self, context):
        m3.clear()

        selection = m3.selected_objects()

        if len(selection) == 1:
            self.setup_weights(selection[0])

        elif len(selection) > 1:
            target = m3.get_active()
            selection.remove(target)

            for obj in selection:
                self.setup_weights(obj)
                self.conform(obj, target)
                m3.make_active(target)

                if self.parent:
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        else:
            pass

        return {'FINISHED'}

    def conform(self, obj, target):
        # for some weird reason, if there's no  bevel mod in the stack, some edges will be set to sharp if you rotate the object around while the shrinkwrap/data transfer is active
        if "Bevel" not in obj.modifiers:
            bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
            bevel.limit_method = "WEIGHT"
            bevel.use_clamp_overlap = False

        if "M3_SurfaceSnapWrap" in obj.modifiers:
            shrink = obj.modifiers.get("M3_SurfaceSnapWrap")
        else:
            shrink = obj.modifiers.new(name="M3_SurfaceSnapWrap", type="SHRINKWRAP")

        shrink.target = target
        shrink.vertex_group = "M3_SurfaceSnap"
        shrink.show_expanded = False

        if "M3_SurfaceSnapTransfer" in obj.modifiers:
            data = obj.modifiers.get("M3_SurfaceSnapTransfer")
        else:
            data = obj.modifiers.new(name="M3_SurfaceSnapTransfer", type="DATA_TRANSFER")

        data.object = target
        data.use_loop_data = True
        data.data_types_loops = {'CUSTOM_NORMAL'}
        data.loop_mapping = 'POLYINTERP_NEAREST'
        data.vertex_group = "M3_SurfaceSnap"
        data.show_expanded = False

    def setup_weights(self, obj):
        active = m3.make_active(obj)

        if "M3_SurfaceSnap" in active.vertex_groups:
            active.vertex_groups.remove(active.vertex_groups.get("M3_SurfaceSnap"))
            # vgroup = active.vertex_groups.get("M3_SurfaceSnap")

        vgroup = active.vertex_groups.new("M3_SurfaceSnap")

        m3.set_mode("EDIT")
        m3.set_mode("FACE")
        m3.unhide_all("MESH")
        m3.select_all("MESH")

        allvids = []

        c = 0
        while c < self.loops:
            c += 1

            bpy.ops.mesh.select_more()
            bpy.ops.mesh.region_to_loop()

            newvids = m3.get_selection("VERT")

            vids = list(set(newvids) - set([vid for vidlist in allvids for vid in vidlist]))
            # print(vids, len(vids))

            allvids.append(vids)

        m3.set_mode("OBJECT")

        # apply weights
        weight = 1
        for idx, vids in enumerate(allvids):
            print(weight)
            vgroup.add(vids, weight, "REPLACE")
            weight -= 1 / self.loops
