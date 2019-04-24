import bpy
from mathutils import Matrix


def parent(obj, parentobj):
    if not parentobj.parent and parentobj.matrix_parent_inverse != Matrix():
        print("Resetting %s's parent inverse matrix, as no parent is defined." % (parentobj.name))
        parentobj.matrix_parent_inverse = Matrix()

    p = parentobj
    while p.parent:
        p = p.parent

    obj.parent = parentobj
    obj.matrix_world = p.matrix_parent_inverse @ obj.matrix_world


def flatten(obj):
    bpy.context.scene.update()

    oldmesh = obj.data

    obj.data = obj.to_mesh(bpy.context.depsgraph, apply_modifiers=True)
    obj.modifiers.clear()

    bpy.data.meshes.remove(oldmesh, do_unlink=True)


def add_vgroup(obj, name="", ids=[], weight=1):
    vgroup = obj.vertex_groups.new(name=name)

    if ids:
        vgroup.add(ids, weight, "ADD")

    return vgroup


def add_facemap(obj, name="", ids=[]):
    fmap = obj.face_maps.new(name=name)

    if ids:
        fmap.add(ids)

    return fmap
