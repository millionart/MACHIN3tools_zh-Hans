import bpy
from bpy.props import BoolProperty, EnumProperty
from mathutils import Matrix, Vector, Euler
from .. utils import MACHIN3 as m3


# TODO: bone support? you can't select a pose bone when in object mode

modeitems = [("ACTIVE", "to Active", ""),
             ("FLOOR", "Floor", "")]
             # ("CURSOR", "Cursor", "")]


class Align(bpy.types.Operator):
    bl_idname = "machin3.align"
    bl_label = "MACHIN3: Align"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Mode", items=modeitems, default="ACTIVE")

    location: BoolProperty(name="Align Location", default=True)
    rotation: BoolProperty(name="Align Rotation", default=True)
    scale: BoolProperty(name="Align Scale", default=False)

    loc_x: BoolProperty(name="X", default=True)
    loc_y: BoolProperty(name="Y", default=True)
    loc_z: BoolProperty(name="Z", default=True)

    rot_x: BoolProperty(name="X", default=True)
    rot_y: BoolProperty(name="Y", default=True)
    rot_z: BoolProperty(name="Z", default=True)

    sca_x: BoolProperty(name="X", default=True)
    sca_y: BoolProperty(name="Y", default=True)
    sca_z: BoolProperty(name="Z", default=True)


    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "mode", expand=True)

        if self.mode == "ACTIVE":
            row = column.split(factor=0.33)
            row.prop(self, "location", text="Location")

            r = row.row(align=True)
            r.active = self.location
            r.prop(self, "loc_x", toggle=True)
            r.prop(self, "loc_y", toggle=True)
            r.prop(self, "loc_z", toggle=True)


            row = column.split(factor=0.33)
            row.prop(self, "rotation", text="Rotation")

            r = row.row(align=True)
            r.active = self.rotation
            r.prop(self, "rot_x", toggle=True)
            r.prop(self, "rot_y", toggle=True)
            r.prop(self, "rot_z", toggle=True)


            row = column.split(factor=0.33)
            row.prop(self, "scale", text="Scale")

            r = row.row(align=True)
            r.active = self.scale
            r.prop(self, "sca_x", toggle=True)
            r.prop(self, "sca_y", toggle=True)
            r.prop(self, "sca_z", toggle=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        sel = m3.selected_objects()

        if self.mode == "ACTIVE":
            active = m3.get_active()

            if active in sel:
                sel.remove(active)

                self.align_to_active(active, sel)

        elif self.mode == "FLOOR":
            self.put_on_floor(sel)


        # elif self.mode == "CURSOR":
            # TODO: align_to_cursor
            # pass

        return {'FINISHED'}

    def put_on_floor(self, selection):
        for obj in selection:
            mx = obj.matrix_world

            if obj.type == "MESH":
                minz = min((mx @ v.co)[2] for v in obj.data.vertices)

                mx.translation.z -= minz

            elif obj.type == "EMPTY":
                mx.translation.z -= obj.location.z


    def align_to_active(self, active, sel):
        # get target matrix and decompose
        amx = active.matrix_world
        aloc, arot, asca = amx.decompose()

        # split components into x,y,z axis elements
        alocx, alocy, alocz = aloc
        arotx, aroty, arotz = arot.to_euler('XYZ')
        ascax, ascay, ascaz = asca

        for obj in sel:
            # get object matrix and decompose
            omx = obj.matrix_world
            oloc, orot, osca = omx.decompose()

            # split components into x,y,z axis elements
            olocx, olocy, olocz = oloc
            orotx, oroty, orotz = orot.to_euler('XYZ')
            oscax, oscay, oscaz = osca

            # TRANSLATION

            # if location is aligned, pick the axis elements based on the loc axis props
            if self.location:
                locx = alocx if self.loc_x else olocx
                locy = alocy if self.loc_y else olocy
                locz = alocz if self.loc_z else olocz

                # re-assemble into translation matrix
                loc = Matrix.Translation(Vector((locx, locy, locz)))

            # otherwise, just use the object's location component
            else:
                loc = Matrix.Translation(oloc)


            # ROTATION

            # if rotation is aligned, pick the axis elements based on the rot axis props
            if self.rotation:
                rotx = arotx if self.rot_x else orotx
                roty = aroty if self.rot_y else oroty
                rotz = arotz if self.rot_z else orotz

                # re-assemble into rotation matrix
                rot = Euler((rotx, roty, rotz), 'XYZ').to_matrix().to_4x4()

            # otherwise, just use the object's rotation component
            else:
                rot = orot.to_matrix().to_4x4()


            # SCALE

            sca = Matrix()

            # if scale is aligned, pick the axis elements based on the sca axis props
            if self.scale:
                scax = ascax if self.sca_x else oscax
                scay = ascay if self.sca_y else oscay
                scaz = ascaz if self.sca_z else oscaz

                # re-assemble into scale matrix
                for i in range(3):
                    sca[i][i] = (scax, scay, scaz)[i]

            # otherwise, just use the object's scale component
            else:
                for i in range(3):
                    sca[i][i] = osca[i]


            # re-combine components into world matrix
            obj.matrix_world = loc @ rot @ sca
