import bpy
from bpy.props import StringProperty, BoolProperty
import os
import re
from ... utils import MACHIN3 as m3


class Save(bpy.types.Operator):
    bl_idname = "machin3.save"
    bl_label = "Save"
    bl_description = "Save"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        currentblend = bpy.data.filepath

        if currentblend:
            bpy.ops.wm.save_mainfile()
            print("Saved blend:", currentblend)
        else:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        return {'FINISHED'}


class SaveIncremental(bpy.types.Operator):
    bl_idname = "machin3.save_incremental"
    bl_label = "Incremental Save"
    bl_description = "Incremental Save"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        currentblend = bpy.data.filepath

        if currentblend:
            incrblend = self.get_incremented_path(currentblend)

            if os.path.exists(incrblend):
                self.report({'ERROR'}, "File '%s' exists already!\nBlend has NOT been saved incrementally!" % (incrblend))
            else:
                bpy.ops.wm.save_as_mainfile(filepath=incrblend)
                print("Saved blend incrementally:", incrblend)
        else:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        return {'FINISHED'}


    def get_incremented_path(self, currentblend):
        path = os.path.dirname(currentblend)
        filename = os.path.basename(currentblend)

        filenameRegex = re.compile(r"(.+)\.blend\d*$")

        mo = filenameRegex.match(filename)

        if mo:
            name = mo.group(1)
            numberendRegex = re.compile(r"(.*?)(\d+)$")

            mo = numberendRegex.match(name)

            if mo:
                basename = mo.group(1)
                numberstr = mo.group(2)
            else:
                basename = name + "_"
                numberstr = "000"

            number = int(numberstr)

            incr = number + 1
            incrstr = str(incr).zfill(len(numberstr))
            incrname = basename + incrstr + ".blend"

            return os.path.join(path, incrname)


class LoadMostRecent(bpy.types.Operator):
    bl_idname = "machin3.load_most_recent"
    bl_label = "Load Most Recent"
    bl_options = {"REGISTER"}

    def execute(self, context):
        recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")

        try:
            with open(recent_path) as file:
                recent_files = file.read().splitlines()
        except (IOError, OSError, FileNotFoundError):
            recent_files = []

        if recent_files:
            most_recent = recent_files[0]

            bpy.ops.wm.open_mainfile(filepath=most_recent, load_ui=True)

        return {'FINISHED'}


class AppendWorld(bpy.types.Operator):
    bl_idname = "machin3.append_world"
    bl_label = "Append World"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return m3.M3_prefs().appendworldpath and m3.M3_prefs().appendworldname

    def draw(self, context):
        layout = self.layout

        column = layout.column()

    def execute(self, context):
        path = m3.M3_prefs().appendworldpath
        name = m3.M3_prefs().appendworldname

        fullpath = "%s/%s" % (path, "World")

        sel = context.selected_objects
        active = context.active_object

        bpy.ops.wm.append(directory=fullpath, filename=name)
        # bpy.context.scene.cycles.film_transparent = False

        world = bpy.data.worlds.get(name)

        if world:
            bpy.context.scene.world = world
        else:
            self.report({'ERROR'}, "World '%s' could not be appended.\nMake sure a world of that name exists in the world source file." % (name))

        # resetting original selection and active which is lost after the append op
        for obj in sel:
            obj.select_set('SELECT')

        bpy.context.view_layer.objects.active = active

        return {'FINISHED'}


class AppendMaterial(bpy.types.Operator):
    bl_idname = "machin3.append_material"
    bl_label = "Append Material"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Append Name")

    applymaterial: BoolProperty(name="Apply Material to Selection", default=True)


    @classmethod
    def poll(cls, context):
        return m3.M3_prefs().appendmatspath

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "applymaterial")

    def execute(self, context):
        path = m3.M3_prefs().appendmatspath
        name = self.name

        fullpath = "%s/%s" % (path, "Material")

        sel = context.selected_objects
        active = context.active_object

        if name == "ALL":
            all_names = [mat.name for mat in m3.M3_prefs().appendmats]

            for name in all_names:
                n = name.replace("-", "")
                bpy.ops.wm.append(directory=fullpath, filename=n)
        else:
            n = name.replace("-", "")
            bpy.ops.wm.append(directory=fullpath, filename=n)

            mat = bpy.data.materials.get(name)

            for obj in sel:
                obj.select_set('SELECT')

                if self.applymaterial:
                    if mat:
                        if not obj.material_slots:
                            bpy.context.view_layer.objects.active = obj
                            bpy.ops.object.material_slot_add()

                        obj.material_slots[0].material = mat
                    else:
                        self.report({'ERROR'}, "Material '%s' could not be appended.\nMake sure a material of that name exists in the material source file." % (n))


        bpy.context.view_layer.objects.active = active

        return {'FINISHED'}


class LoadWorldSource(bpy.types.Operator):
    bl_idname = "machin3.load_world_source"
    bl_label = "Load World Source"
    bl_description = "Load World Source File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return m3.M3_prefs().appendworldpath


    def execute(self, context):
        appendworldpath = m3.M3_prefs().appendworldpath

        if os.path.exists(appendworldpath):
            bpy.ops.wm.open_mainfile(filepath=appendworldpath, load_ui=True)

        return {'FINISHED'}


class LoadMaterialsSource(bpy.types.Operator):
    bl_idname = "machin3.load_materials_source"
    bl_label = "Load Materials Source"
    bl_description = "Load Materials Source File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return m3.M3_prefs().appendmatspath

    def draw(self, context):
        layout = self.layout

        column = layout.column()

    def execute(self, context):
        appendmatspath = m3.M3_prefs().appendmatspath

        if os.path.exists(appendmatspath):
            bpy.ops.wm.open_mainfile(filepath=appendmatspath, load_ui=True)

        return {'FINISHED'}
