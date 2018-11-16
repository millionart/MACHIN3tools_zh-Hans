import bpy
from bpy.props import EnumProperty
from bpy.types import Menu
from .. utils import MACHIN3 as m3
from .. utils.ui import get_icon

# TODO: edit mesh align pie
# TODO: snapping  pie


class PieModes(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_modes"
    bl_label = "Modes"

    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings

        active = context.active_object

        if active:
            if active.type == 'MESH':
                pie = layout.menu_pie()

                # 4 - LEFT
                pie.operator("machin3.vertex_mode", text="Vertex", icon_value=get_icon('vertex'))

                # 6 - RIGHT
                pie.operator("machin3.face_mode", text="Face", icon_value=get_icon('face'))

                # 2 - BOTTOM
                pie.operator("machin3.edge_mode", text="Edge", icon_value=get_icon('edge'))

                # 8 - TOP
                if bpy.context.object.mode == "OBJECT":
                    text = "Edit"
                    icon = get_icon('edit_mesh')
                elif bpy.context.object.mode == "EDIT":
                    text = "Object"
                    icon = get_icon('object')
                pie.operator("machin3.edit_mode", text=text, icon_value=icon)

                # 7 - TOP - LEFT
                if bpy.context.object.mode == "EDIT":
                    pie.prop(context.scene.M3, "pass_through", text="Pass Through" if context.scene.M3.pass_through else "Occlude", icon="XRAY")
                else:
                    pie.separator()

                # 9 - TOP - RIGHT
                pie.separator()

                # 1 - BOTTOM - LEFT
                pie.separator()

                # 3 - BOTTOM - RIGHT
                if bpy.context.object.mode == "EDIT":
                    box = pie.split()
                    column = box.column()
                    column.prop(toolsettings, "use_mesh_automerge", text="Auto Merge")
                else:
                    pie.separator()

            """

            elif ob.object.type == 'EMPTY':
                pass

            elif ob.object.type == 'CURVE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'ARMATURE':
                pie = layout.menu_pie()

                # 4 - LEFT
                pie.operator("object.editmode_toggle", text="Edit Mode", icon='OBJECT_DATAMODE')
                # 6 - RIGHT
                pie.operator("object.posemode_toggle", text="Pose", icon='POSE_HLT')
                # 2 - BOTTOM
                pie.separator()
                # 8 - TOP
                pie.operator("class.object", text="Object Mode", icon='OBJECT_DATAMODE')
                # 7 - TOP - LEFT
                pie.separator()
                # 9 - TOP - RIGHT
                pie.separator()
                # 1 - BOTTOM - LEFT
                pie.separator()
                # 3 - BOTTOM - RIGHT

            elif ob.object.type == 'FONT':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'SURFACE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'META':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'LATTICE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            else:
                pass

            """


class PieSave(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_save"
    bl_label = "Save, Open, Append"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("wm.open_mainfile", text="Open...", icon_value=get_icon('open'))

        # 6 - RIGHT
        pie.operator("machin3.save", text="Save", icon_value=get_icon('save'))

        # 2 - BOTTOM
        pie.operator("wm.save_as_mainfile", text="Save As..", icon_value=get_icon('save_as'))

        # 8 - TOP
        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(column)

        column = box.column()
        b = column.box()
        self.draw_center_column_top(b)

        if bpy.data.filepath:
            b = column.box()
            self.draw_center_column_bottom(b)

        b = box.box()
        column = b.column()
        self.draw_right_column(column)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        pie.operator("machin3.new", text="New", icon_value=get_icon('new'))

        # 3 - BOTTOM - RIGHT
        pie.operator("machin3.save_incremental", text="Incremental Save", icon_value=get_icon('save_incremental'))

    def draw_left_column(self, col):
        col.scale_x = 1.1

        row = col.row()
        row.scale_y = 1.5
        row.operator("machin3.load_most_recent", text="(R) Most Recent", icon_value=get_icon('open_recent'))
        # row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "INFO_MT_file_open_recent"
        row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "TOPBAR_MT_file_open_recent"

        col.separator()
        col.operator("wm.recover_auto_save", text="Recover Auto Save...", icon_value=get_icon('recover_auto_save'))
        # col.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
        col.operator("wm.revert_mainfile", text="Revert", icon_value=get_icon('revert'))

    def draw_center_column_top(self, col):
        row = col.split(factor=0.25)
        row.label(text="Alembic")
        r = row.row(align=True)
        r.operator("wm.alembic_import", text="Import", icon_value=get_icon('import'))
        r.operator("wm.alembic_export", text="Export", icon_value=get_icon('export'))

        row = col.split(factor=0.25)
        row.label(text="Collada")
        r = row.row(align=True)
        r.operator("wm.collada_import", text="Import", icon_value=get_icon('import'))
        r.operator("wm.collada_export", text="Export", icon_value=get_icon('export'))

    def draw_center_column_bottom(self, col):
        row = col.split(factor=0.5)
        row.scale_y = 1.25
        row.operator("machin3.load_previous", text="Previous", icon_value=get_icon('open_previous'))
        row.operator("machin3.load_next", text="Next", icon_value=get_icon('open_next'))

    def draw_right_column(self, col):
        row = col.row()
        r = row.row(align=True)
        r.operator("wm.append", text="Append", icon_value=get_icon('append'))
        r.operator("wm.link", text="Link", icon_value=get_icon('link'))
        row.operator("wm.call_menu", text="", icon_value=get_icon('external_data')).name = "TOPBAR_MT_file_external_data"

        # append world and materials

        appendworldpath = m3.M3_prefs().appendworldpath
        appendmatspath = m3.M3_prefs().appendmatspath

        if any([appendworldpath, appendmatspath]):
            col.separator()

            if appendworldpath:
                row = col.split(factor=0.8)
                row.scale_y = 1.5
                row.operator("machin3.append_world", text="World", icon_value=get_icon('world'))
                row.operator("machin3.load_world_source", text="", icon_value=get_icon('open_world'))

            if appendmatspath:
                row = col.split(factor=0.8)
                row.scale_y = 1.5
                row.operator("wm.call_menu", text="Material", icon_value=get_icon('material')).name = "VIEW3D_MT_MACHIN3_append_materials"
                row.operator("machin3.load_materials_source", text="", icon_value=get_icon('open_material'))


class PieShading(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_shading"
    bl_label = "Shading and Overlays"

    def draw(self, context):
        layout = self.layout

        view = context.space_data

        pie = layout.menu_pie()

        # 4 - LEFT
        text, icon = self.get_text_icon(context, "SOLID")
        pie.operator("machin3.shade_solid", text=text, icon=icon)

        # 6 - RIGHT
        text, icon = self.get_text_icon(context, "MATERIAL")
        pie.operator("machin3.shade_material", text=text, icon=icon)

        # 2 - BOTTOM
        pie.separator()

        # 8 - TOP
        box = pie.split()

        b = box.box()
        column = b.column()
        self.draw_left_column(context, view, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(context, view, column)

        b = box.box()
        column = b.column()
        self.draw_right_column(context, view, column)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        text, icon = self.get_text_icon(context, "WIREFRAME")
        pie.operator("machin3.shade_wire", text=text, icon=icon)

        # 3 - BOTTOM - RIGHT
        text, icon = self.get_text_icon(context, "RENDERED")
        pie.operator("machin3.shade_rendered", text=text, icon=icon)

    def draw_left_column(self, context, view, col):
        row = col.split(factor=0.45)
        row.operator("machin3.toggle_grid", text="Grid Toggle", icon="GRID")
        r = row.split().row(align=True)
        r.active = view.overlay.show_floor
        r.prop(view.overlay, "show_axis_x", text="X", toggle=True)
        r.prop(view.overlay, "show_axis_y", text="Y", toggle=True)
        r.prop(view.overlay, "show_axis_z", text="Z", toggle=True)

        # col.separator()
        row = col.split(factor=0.45)

        icon = get_icon('wireframe_overlay') if view.overlay.show_wireframes else get_icon('wireframe')
        row.operator("machin3.toggle_wireframe", text="Wire Toggle", icon_value=icon)

        r = row.split().row()
        if context.mode == "OBJECT":
            r.active = view.overlay.show_wireframes
            r.prop(view.overlay, "wireframe_threshold", text="Wireframe")
        elif context.mode == "EDIT_MESH":
            r.active = view.shading.show_xray
            r.prop(view.shading, "xray_alpha", text="X-Ray")

        row = col.split(factor=0.45)
        row.operator("machin3.toggle_outline", text="(Q) Outline Toggle")
        row.prop(view.shading, "object_outline_color", text="")

        active = context.active_object
        if active:
            if active.type == "MESH":
                mesh = active.data

                col.separator()
                row = col.split(factor=0.55)
                r = row.split().row(align=True)
                r.operator("machin3.shade_smooth", text="Smooth", icon_value=get_icon('smooth'))
                r.operator("machin3.shade_flat", text="Flat", icon_value=get_icon('flat'))
                row.prop(mesh, "use_auto_smooth")
                if mesh.use_auto_smooth:
                    if mesh.has_custom_normals:
                        col.operator("mesh.customdata_custom_splitnormals_clear", text="Clear Custom Normals")
                    else:
                        col.prop(mesh, "auto_smooth_angle")

                if context.mode == "EDIT_MESH":
                    row = col.row(align=True)
                    row.prop(view.overlay, "show_vertex_normals", text="", icon='NORMALS_VERTEX')
                    row.prop(view.overlay, "show_split_normals", text="", icon='NORMALS_VERTEX_FACE')
                    row.prop(view.overlay, "show_face_normals", text="", icon='NORMALS_FACE')

                    r = row.row(align=True)
                    r.active = view.overlay.show_vertex_normals or view.overlay.show_face_normals or view.overlay.show_split_normals
                    r.prop(view.overlay, "normals_length", text="Size")


        if context.mode == "EDIT_MESH":
            col.separator()
            # row = col.row()
            # row.prop(mesh, "show_edges", text="Edges")
            # row.prop(mesh, "show_faces", text="Faces")

            row = col.row(align=True)
            row.prop(view.overlay, "show_edge_crease", text="Creases", toggle=True)
            row.prop(view.overlay, "show_edge_sharp", text="Sharp", toggle=True)
            row.prop(view.overlay, "show_edge_bevel_weight", text="Bevel", toggle=True)

            if not bpy.app.build_options.freestyle:
                row.prop(view.overlay, "show_edge_seams", text="Seams", toggle=True)

    def draw_center_column(self, context, view, col):
        row = col.split(factor=0.42)
        row.prop(view.overlay, "show_cursor", text="3D Cursor")
        r = row.split().row(align=True)
        r.prop(view.overlay, "show_object_origins", text="Origins")
        r.prop(view.overlay, "show_object_origins_all", text="All")

        col.separator()
        row = col.row()
        row.prop(view.overlay, "show_backface_culling")
        row.prop(view.overlay, "show_face_orientation")
        col.prop(view.overlay, "show_relationship_lines")

        active = context.active_object

        if active:
            col.separator()
            row = col.row()
            row.prop(active, "name", text="")
            row.prop(active, "display_type", text="")

            row = col.row()
            row.prop(active, "show_name", text="Name")
            row.prop(active, "show_axis", text="Axis")
            row.prop(active, "show_in_front", text="In Front")

    def draw_right_column(self, context, view, col):
        if view.shading.type == "SOLID":

            # light type
            row = col.row(align=True)
            # row.scale_y = 1.5
            row.prop(view.shading, "light", expand=True)

            # studio / matcap selection
            if view.shading.light in ["STUDIO", "MATCAP"]:
                row = col.row()
                row.scale_y = 0.6
                row.template_icon_view(view.shading, "studio_light", show_labels=True, scale=3)

            # switch matcap
            if view.shading.light == "MATCAP":
                row = col.row()
                row.operator("machin3.matcap_switch", text="(X) Matcap Switch")
                row.operator('VIEW3D_OT_toggle_matcap_flip', text="Matcap Flip", icon='ARROW_LEFTRIGHT')

            # color type
            row = col.row(align=True)
            row.prop(view.shading, "color_type", expand=True)

            # single color
            if view.shading.color_type == 'SINGLE':
                col.prop(view.shading, "single_color", text="")
            elif view.shading.color_type == 'MATERIAL':
                col.operator("machin3.colorize_materials", icon='MATERIAL')

        elif view.shading.type == "MATERIAL":

            # use scene lights and world
            studio_worlds = [w for w in context.user_preferences.studio_lights if "datafiles/studiolights/world" in w.path]

            if any([bpy.data.lights, studio_worlds]):
                row = col.row()
                if bpy.data.lights:
                    row.prop(view.shading, "use_scene_lights")

                if studio_worlds:
                    row.prop(view.shading, "use_scene_world")

                    # world hdri selection and manipulation
                    if not view.shading.use_scene_world:
                            row = col.row()
                            row.scale_y = 0.6
                            row.template_icon_view(view.shading, "studio_light")

                            col.prop(view.shading, "studiolight_rotate_z", text="Rotation")
                            col.prop(view.shading, "studiolight_background_alpha")

            # world background node props

            if view.shading.use_scene_world or not studio_worlds:
                world = context.scene.world
                if world:
                    if world.use_nodes:
                        tree = context.scene.world.node_tree
                        output = tree.nodes.get("World Output")

                        if output:
                            input_surf = output.inputs.get("Surface")

                            if input_surf:
                                if input_surf.links:
                                    node = input_surf.links[0].from_node

                                    if node.type == "BACKGROUND":
                                        color = node.inputs['Color']
                                        strength = node.inputs['Strength']

                                        if color.links:
                                            col.prop(strength, "default_value", text="Background Strength")
                                        else:
                                            row = col.split(factor=0.7)
                                            row.prop(strength, "default_value", text="Background Strength")
                                            row.prop(color, "default_value", text="")

                                        col.separator()

            # eevee settings

            icon = "TRIA_DOWN" if context.scene.eevee.use_ssr else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_ssr", icon=icon)
            if context.scene.eevee.use_ssr:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "ssr_thickness")
                row.prop(context.scene.eevee, "use_ssr_halfres")


            icon = "TRIA_DOWN" if context.scene.eevee.use_gtao else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_gtao", icon=icon)
            if context.scene.eevee.use_gtao:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "gtao_distance")
                row.prop(context.scene.eevee, "gtao_factor")

            icon = "TRIA_DOWN" if context.scene.eevee.use_bloom else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_bloom", icon=icon)
            if context.scene.eevee.use_bloom:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "bloom_threshold")
                row.prop(context.scene.eevee, "bloom_radius")

            icon = "TRIA_DOWN" if context.scene.eevee.use_volumetric else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_volumetric", icon=icon)
            if context.scene.eevee.use_volumetric:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "volumetric_start")
                row.prop(context.scene.eevee, "volumetric_end")


        elif view.shading.type == "RENDERED":
            col.prop(context.scene.render, "engine")

            col.label(text='TODO: render setting presets')
            col.label(text='TODO: pack images op?')


        elif view.shading.type == "WIREFRAME":
            row = col.row()
            row.prop(view.shading, "show_xray_wireframe", text="")
            row.prop(view.shading, "xray_alpha_wireframe", text="X-Ray")

    def get_text_icon(self, context, shading):
        if context.space_data.shading.type == shading:
            text = "Toggle Overlays"
            icon = "OVERLAY"
        else:
            if shading == "SOLID":
                text = "Solid"
                icon = "SHADING_SOLID"
            elif shading == "MATERIAL":
                text = "LookDev"
                icon = "SHADING_TEXTURE"
            elif shading == "RENDERED":
                text = "Rendered"
                icon = "SHADING_RENDERED"
            elif shading == "WIREFRAME":
                text = "Wireframe"
                icon = "SHADING_WIRE"

        return text, icon


class PieViews(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_views"
    bl_label = "Views and Cams"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ob = bpy.context.object
        # obj = context.object
        scene = context.scene
        view = context.space_data
        r3d = view.region_3d
        # rd = scene.render

        # align_active = bpy.context.scene.machin3.pieviewsalignactive

        # 4 - LEFT
        op = pie.operator("machin3.view_axis", text="Front")
        op.axis='FRONT'

        # 6 - RIGHT
        op = pie.operator("machin3.view_axis", text="Right")
        op.axis='RIGHT'
        # 2 - BOTTOM
        op = pie.operator("machin3.view_axis", text="Top")
        op.axis='TOP'
        # 8 - TOP

        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(scene, view, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(column)

        b = box.box()
        column = b.column()
        self.draw_right_column(view, r3d, column)


        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()


        """
        box = pie.split()
        column = box.column()
        column.scale_x = 0.8


        row = column.row()
        row.label("Resolution")
        row.prop(context.scene.machin3, "preview_percentage", text="")
        row.prop(context.scene.machin3, "final_percentage", text="")

        row = column.row()
        row.label("Samples")
        row.prop(context.scene.machin3, "preview_samples", text="")
        row.prop(context.scene.machin3, "final_samples", text="")

        row = column.row(align=True)
        row.label("Set")
        row.operator("machin3.set_preview", text="Preview")
        row.operator("machin3.set_final", text="Final")

        column.separator()
        column.operator("machin3.pack_images", text="Pack Images")
        column.separator()
        column.separator()
        column.separator()
        # """

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()

    def draw_left_column(self, scene, view, col):
        col.scale_x = 2

        row = col.row()
        row.scale_y = 1.5
        row.operator("machin3.smart_view_cam", text="Smart View Cam", icon='VISIBLE_IPO_ON')


        row = col.split()
        row.operator("machin3.make_cam_active")
        row.prop(scene, "camera", text="")


        row = col.split()
        row.operator("view3d.camera_to_view", text="Cam to view", icon='VIEW_CAMERA')

        text, icon = ("Unlock from View", "UNLOCKED") if view.lock_camera else ("Lock to View", "LOCKED")
        row.operator("wm.context_toggle", text=text, icon=icon).data_path = "space_data.lock_camera"

    def draw_center_column(self, col):
        col.scale_y = 1.5
        op = col.operator("machin3.view_axis", text="Bottom")
        op.axis='BOTTOM'

        row = col.row(align=True)
        op = row.operator("machin3.view_axis", text="Left")
        op.axis='LEFT'

        op = row.operator("machin3.view_axis", text="Back")
        op.axis='BACK'

    def draw_right_column(self, view, r3d, col):
        row = col.row()
        row.scale_y = 1.5
        text, icon = ("Orthographic", "VIEW_ORTHO") if r3d.is_perspective else ("Perspective", "VIEW_PERSPECTIVE")
        row.operator("view3d.view_persportho", text=text, icon=icon)

        col.prop(view, "lens")


class PieAlign(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_align"
    bl_label = "Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        op = pie.operator("machin3.align_editmesh", text="Y min")
        op.axis = "Y"
        op.type = "MIN"

        # 6 - RIGHT
        op = pie.operator("machin3.align_editmesh", text="Y max")
        op.axis = "Y"
        op.type = "MAX"

        # 2 - BOTTOM
        pie.separator()

        # 8 - TOP
        box = pie.split()
        box.scale_y = 1.3

        column = box.column(align=True)
        column.label(icon="FREEZE")
        op = column.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "ZERO"
        op = column.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "ZERO"
        op = column.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "ZERO"

        column = box.column(align=True)
        column.label(icon="ARROW_LEFTRIGHT")
        op = column.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "AVERAGE"
        op = column.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "AVERAGE"
        op = column.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "AVERAGE"

        column = box.column(align=True)
        column.label(icon="PIVOT_CURSOR")
        op = column.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "CURSOR"
        op = column.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "CURSOR"
        op = column.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "CURSOR"

        column.separator()
        column.separator()
        column.separator()

        # 7 - TOP - LEFT
        op = pie.operator("machin3.align_editmesh", text="X min")
        op.axis = "X"
        op.type = "MIN"

        # 9 - TOP - RIGHT
        op = pie.operator("machin3.align_editmesh", text="X max")
        op.axis = "X"
        op.type = "MAX"

        # 1 - BOTTOM - LEFT
        op = pie.operator("machin3.align_editmesh", text="Z min")
        op.axis = "Z"
        op.type = "MIN"

        # 3 - BOTTOM - RIGHT
        op = pie.operator("machin3.align_editmesh", text="Z max")
        op.axis = "Z"
        op.type = "MAX"


class PieWorkspace(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_workspace"
    bl_label = "Workspaces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("machin3.switch_workspace", text="MACHIN3", icon='VIEW3D').name="General"

        # 6 - RIGHT
        pie.separator()
        # pie.operator("machin3.layout_switch", text="Compositing", icon='NODETREE').variable="M3 compositing"

        # 2 - BOTTOM
        pie.operator("machin3.switch_workspace", text="Scripting", icon='CONSOLE').name="Scripting"

        # 8 - TOP
        pie.operator("machin3.switch_workspace", text="Material", icon='MATERIAL_DATA').name="Material"

        # 7 - TOP - LEFT
        pie.operator("machin3.switch_workspace", text="UVs", icon='GROUP_UVS').name="UVs"

        # 9 - TOP - RIGHT
        pie.operator("machin3.switch_workspace", text="World", icon='WORLD').name="World"

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()
        # pie.operator("machin3.layout_switch", text="Video Editing", icon='RENDER_ANIMATION').variable="M3 video"
