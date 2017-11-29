import bpy
import bmesh
from .. import M3utils as m3


vertliststored = []

# TODO: refactor and safety checks


class SlideExtend(bpy.types.Operator):
    bl_idname = "machin3.slide_extend"
    bl_label = "MACHIN3: Slide Extend"
    bl_options = {'REGISTER'}

    def execute(self, context):
        mode = m3.get_mode()

        if mode == "VERT":
            global vertliststored
            # print(vertliststored)

            # SNAPPING CHECK ###

            # check current snapping state
            if bpy.context.scene.tool_settings.use_snap:
                print("Snapping is on!")
                self.snapState = True
                # turn snapping off
                bpy.context.scene.tool_settings.use_snap = False    # works as expected
            else:
                print("Snapping is off!")
                self.snapState = False

            # ORIENTATION from 2 VERT SELECTION ###

            # get current orientation and save it to a variable
            currentOrientation = str(bpy.context.space_data.transform_orientation)

            # create new orientation based on selection
            bpy.ops.transform.create_orientation(name="Topo Slide", use=True, overwrite=True)

            # SELECT ONLY ORIGINAL VERT ###

            mesh = bpy.context.object.data
            bm = bmesh.from_edit_mesh(mesh)

            vertlist = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
            # print(vertlist)
            if len(vertlist) < 2:
                # print("using stored selection history.")
                vertlist = vertliststored
            else:
                # print("created new selection history.")
                vertliststored = vertlist
            firstvert = vertlist[0]

            bpy.ops.mesh.select_all(action='DESELECT')

            # the vertex selection needs to happen in object mode for some reason,
            # so we toggle out of edit mode and in it again at the end
            bpy.ops.object.editmode_toggle()

            obj = bpy.context.active_object.data

            obj.vertices[firstvert].select = True

            bpy.ops.object.editmode_toggle()

            # invoking move tool_
            bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_orientation='Topo Slide', constraint_axis=(False, True, False), release_confirm=True)

            # change the orientation back to what is was before
            bpy.context.space_data.transform_orientation = currentOrientation

        return {'FINISHED'}
