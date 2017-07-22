import bpy
from .. import M3utils as m3


# TODO: if the target is a parent, then you actually want to parent, I think
# TODO: instead of overwriting the ctrl+p menu shortcut, maybe find a way to hook into it?
# TODO: actually you can make this into a tool that does both, child or or parent, just add a switch


class ChildOf(bpy.types.Operator):
    bl_idname = "machin3.child_of"
    bl_label = "MACHIN3: Child Of"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        parent, childs = self.get_parent_and_childs()

        self.add_or_switch_childofs(parent, childs)

        return {'FINISHED'}

    def add_or_switch_childofs(self, parentobject, childobjectlist):
        for c in childobjectlist:
            if "M3 Child Of" in c.constraints:
                print("child of already present")
                # switch between clear inverse and set inverse
                for constraint in c.constraints:
                    if "M3 Child Of" in constraint.name:
                        if type(parentobject) is tuple:
                            # can't make the switch work for this case
                            print("target is armature, not switching")
                        else:
                            parentmatrix = parentobject.matrix_world.inverted()

                            if constraint.inverse_matrix == parentmatrix:
                                print("clearing inverse of '%s'" % (constraint.name))
                                self.childof_clear_inverse(c, constraint)
                            elif constraint.inverse_matrix == c.matrix_parent_inverse:
                                print("setting inverse of '%s'" % (constraint.name))
                                self.childof_set_inverse(c, parentobject, constraint)
                            else:
                                print("parent has been moved, switch manualy between 'set-' and 'clear inverse'")
                                # luckily this usually only has to be set at the beginning
                                # and so, the switching is really just a convinience in case you want a non-standard inverse_matrix

                                # the following doesn't seem to work
                                # m3.make_active(c)
                                # C = bpy.context.copy()
                                # C["constraint"] = constraint
                                # bpy.ops.constraint.childof_set_inverse(C, constraint=constraint.name, owner='OBJECT')
                                # m3.make_active(parentobject)
            else:
                print("creating 'new childof' constraint")
                childof = c.constraints.new("CHILD_OF")
                childof.name = "M3 Child Of"

                if type(parentobject) is tuple:
                    childof.target = parentobject[0]
                    childof.subtarget = parentobject[1].name
                else:
                    childof.target = parentobject

                    # the default mode is 'clear inverse', but we likely want 'set inverse' most of the time(none bone related)
                    self.childof_set_inverse(c, parentobject, childof)

            # update the child data, otherwise, you won't see the effect of set/clear inverse unless you interact with the viewport
            if c.type == "MESH":
                c.data.update()

    def childof_clear_inverse(self, childobject, constraint):
        # setting "clear inverse" - this is default when creating a new child-of constraint
        constraint.inverse_matrix = childobject.matrix_parent_inverse
        childobject.update_tag({'OBJECT'})
        bpy.context.scene.update()

    def childof_set_inverse(self, childobject, parentobject, constraint):
        # setting "set invers"
        # https://blender.stackexchange.com/questions/18562/child-ofs-set-inverse-without-using-bpy-ops
        constraint.inverse_matrix = parentobject.matrix_world.inverted()

        childobject.update_tag({'OBJECT'})
        bpy.context.scene.update()

    def get_parent_and_childs(self):  # returns tuple for active, when active is armature!
        selection = m3.selected_objects()
        active = m3.get_active()
        activebone = None

        selection.remove(active)

        if active.type == "ARMATURE":
            for bone in active.data.bones:
                if bone.select is True:
                    activebone = bone
                    break
            if activebone is None:
                activebone = active.data.bones[0]

        if activebone is not None:
            active = (active, activebone)

        # m3.unselect_all("OBJECT")

        return active, selection
