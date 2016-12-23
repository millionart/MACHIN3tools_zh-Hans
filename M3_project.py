bl_info = {
    "name": "Project",
    "author": "MACHIN3",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "Spacebar Menu/Shift + Alt + E",
    "description": """Wraps around Paul Marshall's "Edge Tools - Project (End Point). Select polygon, fire script, shift select edges and fire it again to project the edges.""",
    "warning": "",
    "wiki_url": "",
    "category": "Interface"}

# SETTINGS

button = "E"
press = "PRESS"
ctrl = False
alt = True
shift = True


import bpy


class Project(bpy.types.Operator):
    bl_idname = "machin3.project"
    bl_label = "MACHIN3: Project"

    def execute(self, context):
        self.project_edge()

        return {'FINISHED'}

    def project_edge(self):
        mode = get_comp_mode()

        if mode == "FACE":
            set_mode("EDGE")
        elif mode == "EDGE":
            bpy.ops.mesh.edgetools_project_end()
        else:
            print("You need to be in FACE or EDGE mode.")


def get_comp_mode():
    subobjtuple = tuple(bpy.context.scene.tool_settings.mesh_select_mode)
    if subobjtuple == (True, False, False):
        # print("edit mode: vertex")
        return "VERT"
    elif subobjtuple == (False, True, False):
        # print("edit mode: edge")
        return "EDGE"
    elif subobjtuple == (False, False, True):
        # print("edit mode: face")
        return "FACE"
    else:
        # print("Unsopported multi sub-object mode")
        return None


def set_mode(string, extend=False, expand=False):
    if string == "EDIT":
        bpy.ops.object.mode_set(mode='EDIT')
    elif string == "OBJECT":
        bpy.ops.object.mode_set(mode='OBJECT')
    elif string in ["VERT", "EDGE", "FACE"]:
        bpy.ops.mesh.select_mode(use_extend=extend, use_expand=expand, type=string)


def register():
    bpy.utils.register_class(Project)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')

    kmi = km.keymap_items.new(Project.bl_idname, button, press, ctrl=ctrl, alt=alt, shift=shift)


def unregister():
    bpy.utils.unregister_class(Project)

    # TODO: properly unregister keymap and keymap_items


if __name__ == "__main__":
    register()
