import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, BoolProperty, EnumProperty
import os
import rna_keymap_ui
from . properties import AppendMatsCollection
from . utils.ui import get_icon



preferences_tabs = [("GENERAL", "General", ""),
                    ("KEYMAPS", "Keymaps", ""),
                    ("ABOUT", "About", "")]


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    path = os.path.dirname(os.path.realpath(__file__))
    bl_idname = os.path.basename(path)

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


    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="Smart Vert", default=True)
    activate_smart_edge: BoolProperty(name="Smart Edge", default=True)
    activate_smart_face: BoolProperty(name="Smart Face", default=True)
    activate_clean_up: BoolProperty(name="Clean Up", default=True)
    activate_clipping_toggle: BoolProperty(name="Clipping Toggle", default=True)
    activate_focus: BoolProperty(name="Focus", default=True)
    activate_mirror: BoolProperty(name="Mirror", default=True)
    activate_align: BoolProperty(name="Align", default=True)


    # MACHIN3pies

    activate_pie_modes: BoolProperty(name="Modes Pie", default=True)
    activate_pie_save: BoolProperty(name="Save Pie", default=True)
    activate_pie_shading: BoolProperty(name="Shading Pie", default=True)
    activate_pie_views: BoolProperty(name="Views Pie", default=True)
    activate_pie_workspace: BoolProperty(name="Workspace Pie", default=False)


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
        row.label(text="Object isolation with history.")

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
        r = row.split(factor=0.4)
        r.label(text="Switch workspaces.")
        r.label(text="If enabled, customize it in ui/pies.py", icon="INFO")


        b = split.box()
        b.label(text="Settings")

        # PIE SAVE

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

            bb = b.box()
            bb.label(text="Matcap Switch")

            column = bb.column()

            row = column.row()

            row.prop(self, "switchmatcap1")
            row.prop(self, "switchmatcap2")

        else:
            b.label(text="Only the Save Pie Menu currently has settings.")

    def draw_keymaps(self, box):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon

        from . keys import keys

        split = box.split()

        b = split.box()
        b.label(text="Tools")

        if not self.draw_tool_keymaps(kc, keys, b):
            b.label(text="No keymappings available, because none the tools have been activated.")


        b = split.box()
        b.label(text="Pie Menus")

        if not self.draw_pie_keymaps(kc, keys, b):
            b.label(text="No keymappings created, because none the pies have been activated.")


    def draw_about(self, box):
        pass


    def draw_tool_keymaps(self, kc, keys, layout):
        drawn = False

        for title in keys:
            items = keys.get(title)

            if "PIE" not in title:
                if self.draw_keymap_items(kc, title, items, layout):
                    drawn = True

        return drawn


    def draw_pie_keymaps(self, kc, keys, layout):
        drawn = False
        for title in keys:
            items = keys.get(title)

            if "PIE" in title:
                if self.draw_keymap_items(kc, title, items, layout):
                    drawn = True

        return drawn


    def draw_keymap_items(self, kc, title, items, layout):
        drawn = False
        for idx, item in enumerate(items):
            keymap = item.get("keymap")

            if keymap:
                km = kc.keymaps.get(keymap)

                kmi = None
                if km:
                    idname = item.get("idname")

                    for kmitem in km.keymap_items:
                        if kmitem.idname == idname:
                            properties = item.get("properties")

                            if properties:
                                if all([getattr(kmitem.properties, name, None) == value for name, value in properties]):
                                    kmi = kmitem
                                    break

                            else:
                                kmi = kmitem
                                break

                # draw keymap item

                if kmi:
                    # multi kmi tools, will only have a single box, created for the first kmi
                    if idx == 0:
                        box = layout.box()

                    # single kmi tools, get their label from the title
                    if len(items) == 1:
                        label = title.title()

                    # multi kmi tools, get it from the label tag, while the title is printed once, before the first item
                    else:
                        if idx == 0:
                            box.label(text=title.title())

                        label = item.get("label")

                    row = box.split(factor=0.15)
                    row.label(text=label)

                    # layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, row, 0)

                    drawn = True
        return drawn
