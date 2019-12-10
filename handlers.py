from bpy.app.handlers import persistent
from . utils.draw import remove_object_axes_drawing_handler


@persistent
def update_object_axes_drawing(none):
    remove_object_axes_drawing_handler()
