import bpy
from bpy.props import BoolProperty
import bmesh


class SmartEdge(bpy.types.Operator):
    bl_idname = "machin3.smart_edge"
    bl_label = "MACHIN3: 智能线"
    bl_options = {'REGISTER', 'UNDO'}

    sharp: BoolProperty(name="Toggle Sharp", default=False)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

    @classmethod
    def poll(cls, context):
        mode = tuple(context.scene.tool_settings.mesh_select_mode)
        return any(mode == m for m in [(True, False, False), (False, True, False), (False, False, True)])

    def execute(self, context):
        active = context.active_object

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        edges = [e for e in bm.edges if e.select]

        # TOGGLE SHARP

        if self.sharp and edges:
            self.toggle_sharp(active, bm, edges)

        # SMART

        else:
            ts = context.scene.tool_settings
            mode = tuple(ts.mesh_select_mode)

            # vert mode
            if mode[0]:
                verts = [v for v in bm.verts if v.select]

                # KNIFE
                if len(verts) <= 1:
                    bpy.ops.mesh.knife_tool('INVOKE_DEFAULT')

                # PATH / STAR CONNECT
                else:

                    # star connects when appropriate, fall back to path connect otherwise
                    connected = self.star_connect(active, bm)

                    if not connected:
                        bpy.ops.mesh.vert_connect_path()

            # edge mode
            elif mode[1]:

                # LOOPCUT
                if len(edges) == 0:
                    bpy.ops.mesh.loopcut_slide('INVOKE_DEFAULT')

                # TURN EDGE
                elif 1 <= len(edges) < 4:
                    bpy.ops.mesh.edge_rotate(use_ccw=False)

                # LOOP TO REGION
                elif len(edges) >= 4:
                    bpy.ops.mesh.loop_to_region()
                    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

            # face mode
            elif mode[2]:
                faces = [f for f in bm.faces if f.select]

                # REGION TO LOOP
                if faces:
                    bpy.ops.mesh.region_to_loop()

                # LOOPCUT
                else:
                    bpy.ops.mesh.loopcut_slide('INVOKE_DEFAULT')

        return {'FINISHED'}

    def toggle_sharp(self, active, bm, edges):
        '''
        sharpen or unsharpen selected edges
        '''

        # existing sharp edges among selection unsharpen
        if any([not e.smooth for e in edges]):
            smooth = True

        # no sharp edges found - sharpen
        else:
            smooth = False

        # (un)sharpen
        for e in edges:
            e.smooth = smooth

        bmesh.update_edit_mesh(active.data)

    def star_connect(self, active, bm):
        '''
        verify the selection and star connect if it fits, otherwise return False
        '''

        def star_connect(bm, last, verts):
            verts.remove(last)

            for v in verts:
                bmesh.ops.connect_verts(bm, verts=[last, v])

        verts = [v for v in bm.verts if v.select]
        history = list(bm.select_history)
        last = history[-1] if history else None

        # check if there's a common face shared by all the verts, a good indicator for star connect
        faces = [f for v in verts for f in v.link_faces]

        common = None
        for f in faces:
            if all([v in f.verts for v in verts]):
                common = f

        # with only two verts, only a path connect makes sence, unless the verts are connected already, then nothing should be done, it works even without a history in the case of just 2
        if len(verts) == 2 and not bm.edges.get([verts[0], verts[1]]):
            return False

        # with 3 verts the base assumption is, you want to make a path connect, common face or not
        elif len(verts) == 3:
            # nothing goes without an active vert
            if last:

                # for path connect you need to have a complete history
                if len(verts) == len(history):
                    return False

                # without a complete history the only option is star connect, but that works only with a common face
                elif common:
                    star_connect(bm, last, verts)


        # with more than 3 verts, the base assumption is, you want to make a star connect, complete history or not
        elif len(verts) > 3:
            # nothing goes without an active vert
            if last:

                # for star connect, you need to have a common face
                if common:
                    star_connect(bm, last, verts)


                # without a common face, the only option is path connect but that needs a complete history
                elif len(verts) == len(history):
                    return False

        bmesh.update_edit_mesh(active.data)
        return True
