import bpy
import bmesh
from bpy.props import BoolProperty
from .. import M3utils as m3


class MirrorX(bpy.types.Operator):
    bl_idname = "machin3.mirror_x"
    bl_label = "MACHIN3: Mirror X"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=True)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=False)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    DMcustomNormals = BoolProperty(name="re-do custom Normals", default=True)
    DMcopiedNormals = BoolProperty(name="move copied Normals to end of stack", default=True)

    def execute(self, context):
        mirror(self)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

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


class MirrorY(bpy.types.Operator):
    bl_idname = "machin3.mirror_y"
    bl_label = "MACHIN3: Mirror Y"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=True)
    axisz = BoolProperty(name="Z", default=False)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    DMcustomNormals = BoolProperty(name="re-do custom Normals", default=True)
    DMcopiedNormals = BoolProperty(name="move copied Normals to end of stack", default=True)

    def execute(self, context):
        mirror(self)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

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


class MirrorZ(bpy.types.Operator):
    bl_idname = "machin3.mirror_z"
    bl_label = "MACHIN3: Mirror Z"
    bl_options = {'REGISTER', 'UNDO'}

    axisx = BoolProperty(name="X", default=False)
    axisy = BoolProperty(name="Y", default=False)
    axisz = BoolProperty(name="Z", default=True)

    DMmirrorU = BoolProperty(name="U", default=True)
    DMmirrorV = BoolProperty(name="V", default=False)

    DMcustomNormals = BoolProperty(name="re-do custom Normals", default=True)
    DMcopiedNormals = BoolProperty(name="move copied Normals to end of stack", default=True)

    def execute(self, context):
        mirror(self)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "axisx", toggle=True)
        row.prop(self, "axisy", toggle=True)
        row.prop(self, "axisz", toggle=True)

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


def mirror(self):
    active = m3.get_active()
    selection = m3.selected_objects()

    if len(selection) > 1:
        selection.remove(active)

        for obj in selection:
            if obj.type in ["MESH", "CURVE"]:
                m3.unselect_all("OBJECT")
                obj.select = True

                mirror = obj.modifiers.new(name="M3_mirror", type="MIRROR")

                mirror.use_x = self.axisx
                mirror.use_y = self.axisy
                mirror.use_z = self.axisz

                mirror.mirror_object = active

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

        for obj in selection:
            obj.select = True

        active.select = True
    else:
        print("Mirror: Select at least 2 objects.")


# TODO: figure out how to do the real mirror  via matrix transforms instead of parenting to and scaling of emptys


class RealMirror(bpy.types.Operator):
    bl_idname = "machin3.real_mirror"
    bl_label = "MACHIN3: Real Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel = m3.selected_objects()

        # create groups to be able to go back to mirrored versions easily
        dupsgroup = bpy.data.groups.get("realmirror_duplicates")
        if not dupsgroup:
            dupsgroup = bpy.data.groups.new("realmirror_duplicates")

        origsgroup = bpy.data.groups.get("realmirror_originals")
        if not origsgroup:
            origsgroup = bpy.data.groups.new("realmirror_originals")


        dups = [obj for obj in sel if obj.type == "MESH"]

        while dups:
            obj = dups[0]

            m3.unselect_all("OBJECT")

            for mod in obj.modifiers:
                if mod.type == "MIRROR":
                    target = mod.mirror_object

                    x = mod.use_x
                    y = mod.use_y
                    z = mod.use_z

                    if mod.show_viewport and mod.show_render and target and any([x, y, z]):
                        print(obj.name, "is mirrored around", target.name)

                        if obj.name not in origsgroup.objects:
                            origsgroup.objects.link(obj)

                        target.hide = False
                        target.select = True
                        m3.make_active(target)

                        bpy.ops.view3d.snap_cursor_to_selected()
                        bpy.ops.transform.create_orientation(use=True)
                        bpy.context.space_data.pivot_point = 'CURSOR'

                        target.select = False

                        empty = bpy.data.objects.new(name="mirror_empty", object_data=None)
                        context.scene.objects.link(empty)

                        if x:
                            print(" » mirroring across", target.name, "X axis")

                            dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (True, False, False))
                            dups.append(dup)

                            if y:
                                dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (True, True, False))
                                dups.append(dup)

                                if z:
                                    dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (True, True, True))
                                    dups.append(dup)

                            if z:
                                dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (True, False, True))
                                dups.append(dup)

                        if y:
                            print(" » mirroring across", target.name, "Y axis")
                            dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (False, True, False))
                            dups.append(dup)

                            if z:
                                dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (False, True, True))
                                dups.append(dup)

                        if z:
                            print(" » mirroring across", target.name, "Z axis")
                            dup = real_mirror(context, obj, mod, target, empty, dupsgroup, (False, False, True))
                            dups.append(dup)

                        # turn off the mirror mod on the originals, but keep them
                        mod.show_viewport = False
                        mod.show_render = False

                        bpy.data.objects.remove(empty)

            # kill all the mirror mods on the dups
            if obj not in sel:
                m3.make_active(obj)
                for mod in obj.modifiers:
                    if mod.type == "MIRROR":
                        bpy.ops.object.modifier_remove(modifier=mod.name)

            dups.remove(obj)


        return {'FINISHED'}


def real_mirror(context, obj, mirrormod, target, empty, dupsgroup, axis_tuple):
    empty.matrix_world = target.matrix_world

    dup = obj.copy()
    dup.data = obj.data.copy()
    context.scene.objects.link(dup)

    dup.select = True
    m3.make_active(dup)


    if dup.DM.isdecal:
        if sum(axis_tuple) != 2:  # don't mirror uvs if the decal is mirrored 2 times
            if mirrormod.use_mirror_u and mirrormod.use_mirror_v:
                uv_mirror((True, True, False))
            elif mirrormod.use_mirror_u:
                uv_mirror((True, False, False))
            elif mirrormod.use_mirror_v:
                uv_mirror((False, True, False))

        for mod in dup.modifiers:
            if mod.type == "DATA_TRANSFER" and mod.name == "M3_copied_normals":
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
            if mod.type == "DISPLACE":
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

    bpy.ops.object.modifier_remove(modifier=mirrormod.name)

    empty.select = True
    m3.make_active(empty)
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    bpy.ops.transform.resize(value=(-1, -1, -1), constraint_axis=axis_tuple, constraint_orientation='LOCAL')

    m3.make_active(dup)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    if sum(axis_tuple) != 2:  # don't flip the normals if the obj is mirrored 2 times
        bm = bmesh.new()
        bm.from_mesh(dup.data)

        for f in bm.faces:
            f.normal_flip()

        bm.to_mesh(dup.data)
        bm.normal_update()
        bm.free()

    dup.select = False
    empty.select = False

    if dup.name not in dupsgroup.objects:
        dupsgroup.objects.link(dup)

    return dup


def uv_mirror(axis_tuple):
    m3.set_mode("EDIT")
    m3.unhide_all("MESH")
    m3.select_all("MESH")

    # change context to UV editor
    area = bpy.context.area
    old_type = area.type
    area.type = 'IMAGE_EDITOR'

    bpy.ops.transform.mirror(constraint_axis=axis_tuple, constraint_orientation='GLOBAL')

    # change the context back to what it was
    area.type = old_type

    m3.unselect_all("MESH")
    m3.set_mode("OBJECT")
