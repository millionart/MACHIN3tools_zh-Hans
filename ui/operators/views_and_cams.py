import bpy
from bpy.props import EnumProperty
from ... utils import MACHIN3 as m3


axisitems = [("FRONT", "Front", ""),
             ("BACK", "Back", ""),
             ("LEFT", "Left", ""),
             ("RIGHT", "Right", ""),
             ("TOP", "Top", ""),
             ("BOTTOM", "Bottom", "")]


class ViewAxis(bpy.types.Operator):
    bl_idname = "machin3.view_axis"
    bl_label = "View Axis"
    bl_description = "Click: Align View\nALT + Click: Align View to Active"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(name="Axis", items=axisitems, default="FRONT")


    def invoke(self, context, event):

        if event.alt:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=True)
        else:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=False)

        return {'FINISHED'}


class MakeCamActive(bpy.types.Operator):
    bl_idname = "machin3.make_cam_active"
    bl_label = "Make Active"
    bl_description = "Make selected Camera active."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active:
            return active.type == "CAMERA"

    def execute(self, context):
        context.scene.camera = context.active_object

        return {'FINISHED'}


class SmartViewCam(bpy.types.Operator):
    bl_idname = "machin3.smart_view_cam"
    bl_label = "Smart View Cam"
    bl_description = "Default: View Active Scene Camera\nNo Camera in the Scene: Create Camera from View\nCamera Selected: Make Selected Camera active and view it.\nAlt + Click: Create Camera from current View."
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        scene_cams = [obj for obj in context.scene.objects if obj.type == "CAMERA"]
        view = context.space_data

        # create camera from view
        if not scene_cams or event.alt:
            bpy.ops.object.camera_add()
            context.scene.camera = context.active_object
            bpy.ops.view3d.camera_to_view()

        # view the active cam, or make cam active and view it if active obj is camera
        else:
            active = context.active_object

            if active:
                if active in context.selected_objects and active.type == "CAMERA":
                    context.scene.camera = active

            # if the viewport is already aligned to a camera, toggle two times perspective/ortho. If you stay in cammera mode, the view camera op below will throw an exception. Two times, so you dont swich from perp to ortho
            if view.region_3d.view_perspective == 'CAMERA':
                bpy.ops.view3d.view_persportho()
                bpy.ops.view3d.view_persportho()

            bpy.ops.view3d.view_camera()
            bpy.ops.view3d.view_center_camera()

        return {'FINISHED'}
