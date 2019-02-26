
def set_xray(context):
    x = (context.scene.M3.pass_through, context.scene.M3.show_edit_mesh_wire)
    shading = context.space_data.shading

    shading.show_xray = True if any(x) else False

    if context.scene.M3.show_edit_mesh_wire:
        shading.xray_alpha = 0.1

    elif context.scene.M3.pass_through:
        shading.xray_alpha = 1 if context.active_object and context.active_object.type == "MESH" else 0.5


def reset_xray(context):
    shading = context.space_data.shading

    shading.show_xray = False
    shading.xray_alpha = 0.5
