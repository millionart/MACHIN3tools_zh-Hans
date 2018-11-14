import bpy
from bpy.props import BoolProperty
from .. import M3utils as m3


class CleanoutMaterials(bpy.types.Operator):
    bl_idname = "machin3.cleanout_materials"
    bl_label = "MACHIN3: Cleanout Materials"
    bl_options = {'REGISTER', 'UNDO'}

    changedrawtype = BoolProperty(name="Change Drawtype", default=True)
    changeshading = BoolProperty(name="Change to Material Shading", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "changedrawtype")
        column.prop(self, "changeshading")

    def execute(self, context):

        self.cleanout_materials()

        return {'FINISHED'}

    def cleanout_materials(self):
        global changedrawtype
        didunhide = False

        sel = m3.selected_objects()
        if len(sel) == 0:
            print("\nNothing selected, going over all the scene's Mesh objects.")
            scope = bpy.data.objects
        else:
            scope = sel

        for obj in scope:
            if obj.type == "MESH":
                slots = obj.material_slots
                if len(slots) > 0:
                    m3.make_active(obj, silent=True)
                    print("%s:" % (obj.name))

                    # Make drawtype textured, so they will display materials or lack of them properly in the viewport, once you are in material shading
                    if self.changedrawtype:
                        self.change_drawtype(obj)

                    if obj.hide:
                        print(" > is hidden - unhiding.")
                        obj.hide = False
                        didunhide = True

                    for slot in slots:
                        try:
                            bpy.ops.object.material_slot_remove()
                            print("\t removed slot: '%s'" % (slot.name))
                        except:
                            print(m3.red("Something went wrong removing '%s's' slot '%s'.") % (obj.name, slot.name))

                    if didunhide:
                        print(" > hiding '%s' again." % (obj.name))
                        obj.hide = True

                        didunhide = False
                else:
                    print("'%s' has no material slots." % (obj.name))

        # this will still leave the materials in the scene however
        # the following will remove the materials from the scene
        # it is of utmost importance to only run this, once the magterials are no longer assgigned to objects,
        # otherwise selecting an object/openin the material panel will crash blender

        if len(sel) == 0:
            print(20 * "-")
            print("\nPurging materials from scene.")

            # Clear the user count of a datablock so its not saved, on reload the data will be removed
            # This function is for advanced use only, misuse can crash blender since the user count is used to prevent data being removed when it is used.

            for material in bpy.data.materials:
                print("Removing material: '%s'." % (material.name))
                material.user_clear()
                bpy.data.materials.remove(material)

        if self.changeshading:
            bpy.context.space_data.viewport_shade = "MATERIAL"

    def change_drawtype(self, object):
        try:
            drawtype = bpy.context.object.draw_type
            if drawtype == "SOLID":
                    print('\t changing drawtype to "TEXTURED"')
                    bpy.context.object.draw_type = "TEXTURED"
        except:
            print(m3.red("Something went wrong changing '%s's' drawtype to 'TEXTURED'.") % (object.name))
