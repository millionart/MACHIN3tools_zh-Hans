import bpy
from bpy.props import FloatProperty
from .. import M3utils as m3


# INFO: to be used together with Numpad 0, Ctrl + Numpad 0 + Home keys

# TODO: extend so that each camera can hold a bunch of parameters,
# >>>>: related to the rendering, light light settings, world node settings(such as environment roration),
# >>>>: compositer node settings, etc

# NOTE: theres an issue with adjusing any of the operator props. a workarround is hitting the key combo 2 times in a row

class CameraHelper(bpy.types.Operator):
    bl_idname = "machin3.camera_helper"
    bl_label = "MACHIN3: Camera Helper"
    bl_options = {'REGISTER', 'UNDO'}

    lens = FloatProperty(name="Zoom (Lens)", default=20, min=0)
    camx = FloatProperty(name="Truck (Horizonal)", default=0)
    camy = FloatProperty(name="Pedestal (Vertical)", default=0)
    camz = FloatProperty(name="Dolly", default=0)

    clippingend = FloatProperty(name="Clipping End", default=1000, min=0)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "lens")
        column.prop(self, "camx")
        column.prop(self, "camy")
        column.prop(self, "camz")

        column.separator()
        column.prop(self, "clippingend")

    def execute(self, context):
        active = m3.get_active()

        if active is not None:
            if "camera" in active.name.lower() and active in m3.selected_objects():  # camera should be active AND selected, only then do you change it's location
                print("Camera selected")
                bpy.ops.view3d.object_as_camera()
                try:
                    bpy.ops.view3d.camera_to_view()
                    print("Aligned '%s' to view." % (active.name))
                except:
                    print("View is already aligned to '%s'" % (active.name))
                bpy.ops.view3d.view_center_camera()
                camera = active
            else:  # in case some other object is active
                print("No Camera selected")
                camera = self.create_cam()
                bpy.ops.view3d.camera_to_view()
                bpy.ops.view3d.view_center_camera()
        else:  # in case nothing at all is active(as in after deleting an object)
            print("Nothing selected")
            camera = self.create_cam()
            bpy.ops.view3d.camera_to_view()
            bpy.ops.view3d.view_center_camera()

        # adjusting clipping end, which is 100 by default and a bit on the small side
        camera.data.clip_end = self.clippingend

        # for whatever reason, setting the camera to lens 20, is essentially identical to the viewport camera(n panel) being 35
        camera.data.lens = self.lens

        # make cameras active, so it can be moved/rotated
        m3.unselect_all("OBJECT")
        camera.select = True
        m3.make_active(camera)

        # camera movements, for some reason, this needs to happen in 3 seperate ops, each time with the axis contrained accordingly
        bpy.ops.transform.translate(value=(self.camx, 0, 0), constraint_orientation='LOCAL', constraint_axis=(True, False, False), release_confirm=True)
        bpy.ops.transform.translate(value=(0, self.camy, 0), constraint_orientation='LOCAL', constraint_axis=(False, True, False), release_confirm=True)
        bpy.ops.transform.translate(value=(0, 0, self.camz), constraint_orientation='LOCAL', constraint_axis=(False, False, True), release_confirm=True)

        return {'FINISHED'}

    def create_cam(self):
        cam = bpy.data.cameras.new("Camera")
        cam_obj = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.objects.link(cam_obj)
        print("Created '%s'" % (cam_obj.name))
        # make the new camera the active/scene camera
        bpy.context.scene.camera = cam_obj
        return cam_obj
