import bpy
from mathutils import Vector
import gpu
from gpu_extras.batch import batch_for_shader
import bgl
from .. colors import red, green, blue


def add_object_axes_drawing_handler(dns, args):
    # print("adding object axes drawing handler")

    handler = bpy.types.SpaceView3D.draw_handler_add(draw_object_axes, (args,), 'WINDOW', 'POST_VIEW')
    dns['draw_object_axes'] = handler


def remove_object_axes_drawing_handler(handler=None):
    # print("attempting to remove object axes drawing handler")

    if not handler:
        handler = bpy.app.driver_namespace.get('draw_object_axes')


    if handler:
        # print(" REMOVING object axes drawing handler")

        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        del bpy.app.driver_namespace['draw_object_axes']


def draw_object_axes(args):
    context, objs = args

    if context.space_data.overlay.show_overlays:
        axes = [(Vector((1, 0, 0)), red), (Vector((0, 1, 0)), green), (Vector((0, 0, 1)), blue)]

        size = context.scene.M3.object_axes_size
        alpha = context.scene.M3.object_axes_alpha

        for axis, color in axes:
            coords = []

            for obj in objs:
                mx = obj.matrix_world
                origin, _, _ = mx.decompose()

                # coords.append(origin)
                coords.append(origin + mx.to_3x3() @ axis * size * 0.1)
                coords.append(origin + mx.to_3x3() @ axis * size)

            indices = [(i, i + 1) for i in range(0, len(coords), 2)]

            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            shader.bind()
            shader.uniform_float("color", (*color, alpha))

            bgl.glEnable(bgl.GL_BLEND)
            bgl.glDisable(bgl.GL_DEPTH_TEST)

            bgl.glLineWidth(2)

            batch = batch_for_shader(shader, 'LINES', {"pos": coords}, indices=indices)
            batch.draw(shader)
