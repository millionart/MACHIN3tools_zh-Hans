import bpy
from mathutils import Matrix


def parent(obj, parentobj):
    if not parentobj.parent and parentobj.matrix_parent_inverse != Matrix():
        print("WARNING: Resetting %s's parent inverse matrix, as no parent is defined." % (parentobj.name))
        parentobj.matrix_parent_inverse = Matrix()

    p = parentobj
    while p.parent:
        p = p.parent

    obj.parent = parentobj
    obj.matrix_world = p.matrix_parent_inverse @ obj.matrix_world


def unparent(obj):
    if obj.parent:
        p = obj.parent
        while p.parent:
            p = p.parent

        obj.parent = None
        obj.matrix_world = p.matrix_parent_inverse.inverted_safe() @ obj.matrix_world


def flatten(obj, depsgraph=None):
    if not depsgraph:
        depsgraph = bpy.context.evaluated_depsgraph_get()

    oldmesh = obj.data

    obj.data = bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph))
    obj.modifiers.clear()

    # remove the old mesh
    bpy.data.meshes.remove(oldmesh, do_unlink=True)


def add_vgroup(obj, name="", ids=[], weight=1, debug=False):
    vgroup = obj.vertex_groups.new(name=name)

    if debug:
        print(" » Created new vertex group: %s" % (name))

    if ids:
        vgroup.add(ids, weight, "ADD")

    # from selection
    else:
        obj.vertex_groups.active_index = vgroup.index
        bpy.ops.object.vertex_group_assign()

    return vgroup


def add_facemap(obj, name="", ids=[]):
    fmap = obj.face_maps.new(name=name)

    if ids:
        fmap.add(ids)

    return fmap
