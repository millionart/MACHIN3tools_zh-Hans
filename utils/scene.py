import bpy
from mathutils import Vector, Quaternion


def set_cursor(location=Vector(), rotation=Quaternion()):
    """
    set cursor location (Vector), and rotation (Quaternion)
    note, that setting cursor.matrix has no effect unfortunately
    """

    cursor = bpy.context.scene.cursor

    # set location
    if location:
        cursor.location = location

    # set rotation
    if rotation:
        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion = rotation

        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle = rotation.to_axis_angle()

        else:
            cursor.rotation_euler = rotation.to_euler(cursor.rotation_mode)
