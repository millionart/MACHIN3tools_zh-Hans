import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, PointerProperty, BoolProperty, EnumProperty
import os
import rna_keymap_ui
from . properties import AppendMatsCollection
from . ui.UILists import AppendMatsUIList
from . icons import get_icon



preferences_tabs = [("GENERAL", "General", ""),
                    ("KEYMAPS", "Keymaps", ""),
                    ("ABOUT", "About", "")]


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    bl_idname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.user_preferences.studio_lights if "datafiles/studiolights/matcap" in mc.path]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "NOT FOUND"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.user_preferences.studio_lights if "datafiles/studiolights/matcap" in mc.path]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "NOT FOUND"


    # PROPERTIES

    appendworldpath: StringProperty(name="World Source .blend", subtype='FILE_PATH')
    appendworldname: StringProperty(name="Name of World")

    appendmatspath: StringProperty(name="Materials Source .blend", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty(name="Name of Material to appand")


    switchmatcap1: StringProperty(name="Matcap 1", update=update_switchmatcap1)
    switchmatcap2: StringProperty(name="Matcap 2", update=update_switchmatcap2)

    # MACHIN3pies

    activate_pie_modes: BoolProperty(name="Modes Pie", default=True)
    activate_pie_save: BoolProperty(name="Save Pie", default=True)
    activate_pie_shading: BoolProperty(name="Shading Pie", default=True)
    activate_pie_views: BoolProperty(name="Views Pie", default=True)
    activate_pie_workspace: BoolProperty(name="Workspace Pie", default=True)

    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="Smart Vert", default=True)
    activate_smart_edge: BoolProperty(name="Smart Edge", default=True)
    activate_smart_face: BoolProperty(name="Smart Face", default=True)
    activate_clean_up: BoolProperty(name="Clean Up", default=True)
    activate_clipping_toggle: BoolProperty(name="Clipping Toggle", default=True)
    activate_focus: BoolProperty(name="Focus", default=True)
    activate_mirror: BoolProperty(name="Mirror", default=True)
    activate_align: BoolProperty(name="Align", default=True)

    # hidden

    avoid_update: BoolProperty(default=False)
    tabs: EnumProperty(name="Tabs", items=preferences_tabs, default="KEYMAPS")


    def draw(self, context):
        layout=self.layout


        # TAB BAR

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = column.box()

        if self.tabs == "GENERAL":
            self.draw_general(box)

        elif self.tabs == "KEYMAPS":
            self.draw_keymaps(box)

        elif self.tabs == "ABOUT":
            self.draw_general(box)


    def draw_general(self, box):
        split = box.split()

        b = split.box()
        b.label(text="Activate")


        # MACHIN3tools

        bb = b.box()
        bb.label(text="Tools")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_vert", toggle=True)
        row.label(text="Smart vertex manipulation.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_edge", toggle=True)
        row.label(text="Smart edge creation, manipulation and selection conversion.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_face", toggle=True)
        row.label(text="Smart face creation and object-from-face creation.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clean_up", toggle=True)
        row.label(text="Quick geometry clean up.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clipping_toggle", toggle=True)
        row.label(text="Viewport clipping plane toggle.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_focus", toggle=True)
        row.label(text="Object isolatino with history.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mirror", toggle=True)
        row.label(text="Object-across-object mirroring.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align", toggle=True)
        row.label(text="Object per-axis location, rotation and scale alignment.")


        # MACHIN3pies

        bb = b.box()
        bb.label(text="Pie Menus")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_pie_modes", toggle=True)
        row.label(text="Quick mode changing.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_pie_save", toggle=True)
        row.label(text="Save, open, append. Load recent, previous and next. Append World and Materials.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_pie_shading", toggle=True)
        row.label(text="Control shading, overlays, eevee and some object properties.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_pie_views", toggle=True)
        row.label(text="Control views. Create and manage cameras.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_pie_workspace", toggle=True)
        row.label(text="Switch workspaces.")


        b = split.box()
        b.label(text="Settings")

        # APPEND WORLD AND MATERIALS

        if self.activate_pie_save:
            bb = b.box()
            bb.label(text="Append World and Materials")

            column = bb.column()

            column.prop(self, "appendworldpath")
            column.prop(self, "appendworldname")
            column.separator()

            column.prop(self, "appendmatspath")


            column = bb.column()

            row = column.row()
            rows = len(self.appendmats) if len(self.appendmats) > 6 else 6
            row.template_list("AppendMatsUIList", "", self, "appendmats", self, "appendmatsIDX", rows=rows)

            c = row.column(align=True)
            c.operator("machin3.move_appendmat", text="", icon='TRIA_UP').direction = "UP"
            c.operator("machin3.move_appendmat", text="", icon='TRIA_DOWN').direction = "DOWN"

            c.separator()
            c.separator()
            c.operator("machin3.rename_appendmat", text="", icon='OUTLINER_DATA_FONT')
            c.separator()
            c.separator()
            c.operator("machin3.clear_appendmats", text="", icon='LOOP_BACK')
            c.operator("machin3.remove_appendmat", text="", icon_value=get_icon('cancel'))

            row = column.row()
            row.prop(self, "appendmatsname")
            row.operator("machin3.add_appendmat", text="", icon_value=get_icon('plus'))


            # MATCAP SWITCH

            column.separator()
            row = column.row()

            row.prop(self, "switchmatcap1")
            row.prop(self, "switchmatcap2")

        else:
            b.label(text="Only the Save Pie Menu currently has settings.")

    def draw_keymaps(self, box):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon


        split = box.split()

        b = split.box()
        b.label(text="Tools")

        if self.activate_smart_vert:
            bb = b.box()
            bb.label(text="Smart Vert")
            self.draw_keymap_item(bb, "Merge Last", kc, "Mesh", "machin3.smart_vert", properties=[("type", "LAST"), ("slide_override", False)], multiple=True)
            self.draw_keymap_item(bb, "Merge Center", kc, "Mesh", "machin3.smart_vert", properties=[("type", "CENTER"), ("slide_override", False)], multiple=True)
            self.draw_keymap_item(bb, "Merge Smart", kc, "Mesh", "machin3.smart_vert", properties=[("type", "SMART"), ("slide_override", False)], multiple=True)
            self.draw_keymap_item(bb, "Slide Extend", kc, "Mesh", "machin3.smart_vert", properties=[("slide_override", True)], multiple=True)

        if self.activate_smart_edge:
            self.draw_keymap_item(b, "Smart Edge", kc, "Mesh", "machin3.smart_edge")

        if self.activate_smart_face:
            self.draw_keymap_item(b, "Smart Face", kc, "Mesh", "machin3.smart_face")

        if self.activate_clean_up:
            self.draw_keymap_item(b, "Clean Up", kc, "Mesh", "machin3.clean_up")

        if self.activate_clipping_toggle:
            self.draw_keymap_item(b, "Clipping Toggle", kc, "3D View Generic", "machin3.clipping_toggle")

        if self.activate_focus:
            self.draw_keymap_item(b, "Focus", kc, "Object Mode", "machin3.focus")

        if self.activate_mirror:
            bb = b.box()
            bb.label(text="Mirror")
            self.draw_keymap_item(bb, "X Axis", kc, "Object Mode", "machin3.mirror", properties=[("use_x", True)], multiple=True)
            self.draw_keymap_item(bb, "Y Axis", kc, "Object Mode", "machin3.mirror", properties=[("use_y", True)], multiple=True)
            self.draw_keymap_item(bb, "Z Axis", kc, "Object Mode", "machin3.mirror", properties=[("use_z", True)], multiple=True)

        if self.activate_align:
            self.draw_keymap_item(b, "Align", kc, "Object Mode", "machin3.align")


        b = split.box()
        b.label(text="Pie Menus")

        if self.activate_pie_modes:
            self.draw_keymap_item(b, "Modes", kc, "Object Non-modal", "wm.call_menu_pie", properties=[("name", "VIEW3D_MT_MACHIN3_modes")])

        if self.activate_pie_save:
            self.draw_keymap_item(b, "Save", kc, "Window", "wm.call_menu_pie", properties=[("name", "VIEW3D_MT_MACHIN3_save")])

        if self.activate_pie_shading:
            self.draw_keymap_item(b, "Shading", kc, "3D View Generic", "wm.call_menu_pie", properties=[("name", "VIEW3D_MT_MACHIN3_shading")])

        if self.activate_pie_views:
            self.draw_keymap_item(b, "Views", kc, "3D View Generic", "wm.call_menu_pie", properties=[("name", "VIEW3D_MT_MACHIN3_views")])

        if self.activate_pie_workspace:
            self.draw_keymap_item(b, "Workspace", kc, "Window", "wm.call_menu_pie", properties=[("name", "VIEW3D_MT_MACHIN3_workspace")])

    def draw_about(self, box):
        pass

    def draw_keymap_item(self, layout, label, kc, keymap, idname, properties=[], multiple=False):
        """
        keymap = "Mesh"
        idname = "machin3.smart_vert"
        properties = [("type", "LAST"), ("slide_override", False)]
        """

        km = kc.keymaps.get(keymap)

        kmi = None
        if km:
            for item in km.keymap_items:
                if item.idname == idname:
                    if properties:
                        if all([getattr(item.properties, attr, None) == value for attr, value in properties]):
                            kmi = item
                            break

                    else:
                        kmi = item
                        break

        if multiple:
            # don't create a box, it's created outside instead and covers multiple items
            row = layout.split(factor=0.15)

        else:
            # create a box
            box = layout.box()
            row = box.split(factor=0.15)

        row.label(text=label)

        if kmi:
            # layout.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, row, 0)

        else:
            row.label(text="Keymapping not found for this item!")
