import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, BoolProperty, EnumProperty
import os
import rna_keymap_ui
from . properties import AppendMatsCollection
from . utils.ui import get_icon
from . utils.registration import activate, get_path, get_name


preferences_tabs = [("GENERAL", "常规", ""),
                    ("KEYMAPS", "键盘映射", ""),
                    ("ABOUT", "关于", "")]


links = [("Documentation", "https://machin3.io/MACHIN3tools/docs/", "INFO"),
         ("MACHINƎ.io", "https://machin3.io", "WORLD"),
         ("Youtube", "https://www.youtube.com/channel/UC4yaFzFDILd2yAqOWRuLOvA", "NONE"),
         ("Twitter", "https://twitter.com/machin3io", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("DECALmachine", "https://machin3.io/DECALmachine", "NONE"),
         ("MESHmachine", "https://machin3.io/MESHmachine", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("MACHINƎ @ Artstation", "https://www.artstation.com/artist/machin3", "NONE"),
         ("", "", ""),
         ]


# TODO: check if the aeppend world/materials paths exist and make them abosolute


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    path = get_path()
    bl_idname = get_name()


    # APPENDMATS

    def update_appendmatsname(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        else:
            if self.appendmatsname and self.appendmatsname not in self.appendmats:
                am = self.appendmats.add()
                am.name = self.appendmatsname

                self.appendmatsIDX = len(self.appendmats) - 1

            self.avoid_update = True
            self.appendmatsname = ""


    # CHECKS

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "没有找到"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "没有找到"

    def update_custom_preferences_keymap(self, context):
        if self.custom_preferences_keymap:
            kc = context.window_manager.keyconfigs.user

            for km in kc.keymaps:
                if km.is_user_modified:
                    self.custom_preferences_keymap = False
                    self.dirty_keymaps = True
                    return

            self.dirty_keymaps = False


    # RUNTIME TOOL ACTIVATION

    def update_activate_smart_vert(self, context):
        activate(self, register=self.activate_smart_vert, tool="smart_vert")

    def update_activate_smart_edge(self, context):
        activate(self, register=self.activate_smart_edge, tool="smart_edge")

    def update_activate_smart_face(self, context):
        activate(self, register=self.activate_smart_face, tool="smart_face")

    def update_activate_clean_up(self, context):
        activate(self, register=self.activate_clean_up, tool="clean_up")

    def update_activate_clipping_toggle(self, context):
        activate(self, register=self.activate_clipping_toggle, tool="clipping_toggle")

    def update_activate_focus(self, context):
        activate(self, register=self.activate_focus, tool="focus")

    def update_activate_mirror(self, context):
        activate(self, register=self.activate_mirror, tool="mirror")

    def update_activate_align(self, context):
        activate(self, register=self.activate_align, tool="align")

    def update_activate_customize(self, context):
        activate(self, register=self.activate_customize, tool="customize")

    # RUNTIME PIE ACTIVATION

    def update_activate_modes_pie(self, context):
        activate(self, register=self.activate_modes_pie, tool="modes_pie")

    def update_activate_save_pie(self, context):
        activate(self, register=self.activate_save_pie, tool="save_pie")

    def update_activate_shading_pie(self, context):
        activate(self, register=self.activate_shading_pie, tool="shading_pie")

    def update_activate_views_pie(self, context):
        activate(self, register=self.activate_views_pie, tool="views_pie")

    def update_activate_align_pie(self, context):
        activate(self, register=self.activate_align_pie, tool="align_pie")

    def update_activate_cursor_pie(self, context):
        activate(self, register=self.activate_cursor_pie, tool="cursor_pie")

    def update_activate_workspace_pie(self, context):
        activate(self, register=self.activate_workspace_pie, tool="workspace_pie")


    # RUNTIME MENU ACTIVATION

    def update_activate_object_specials_menu(self, context):
        activate(self, register=self.activate_object_specials_menu, tool="object_specials_menu")


    # PROPERTIES

    appendworldpath: StringProperty(name="世界环境源 .blend", subtype='FILE_PATH')
    appendworldname: StringProperty(name="世界环境名称")

    appendmatspath: StringProperty(name="材质源 .blend", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty(name="添加的材质名称", update=update_appendmatsname)

    switchmatcap1: StringProperty(name="材质捕获 1", update=update_switchmatcap1)
    switchmatcap2: StringProperty(name="材质捕获 2", update=update_switchmatcap2)

    obj_mode_rotate_around_active: BoolProperty(name="围绕选择项旋转，但只在物体模式下", default=False)
    toggle_cavity: BoolProperty(name="切换 空腔/曲率 在编辑模式下禁用 在物体模式下启用", default=True)

    custom_theme: BoolProperty(name="主题", default=True)
    custom_matcaps: BoolProperty(name="材质捕获 (Matcaps) 和默认着色", default=True)
    custom_overlays: BoolProperty(name="遮罩", default=True)
    custom_preferences_interface: BoolProperty(name="首选项：界面", default=True)
    custom_preferences_viewport: BoolProperty(name="首选项：视口", default=True)
    custom_preferences_navigation: BoolProperty(name="首选项：导航", default=True)
    custom_preferences_keymap: BoolProperty(name="首选项：键盘映射", default=False, update=update_custom_preferences_keymap)
    custom_preferences_system: BoolProperty(name="首选项：系统", default=False)
    custom_preferences_save: BoolProperty(name="首选项：保存和载入", default=True)


    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="智能点", default=True, update=update_activate_smart_vert)
    activate_smart_edge: BoolProperty(name="智能线", default=True, update=update_activate_smart_edge)
    activate_smart_face: BoolProperty(name="智能面", default=True, update=update_activate_smart_face)
    activate_clean_up: BoolProperty(name="清理", default=True, update=update_activate_clean_up)
    activate_clipping_toggle: BoolProperty(name="裁剪切换", default=True, update=update_activate_clipping_toggle)
    activate_focus: BoolProperty(name="聚焦", default=True, update=update_activate_focus)
    activate_mirror: BoolProperty(name="镜射", default=True, update=update_activate_mirror)
    activate_align: BoolProperty(name="对齐", default=True, update=update_activate_align)
    activate_customize: BoolProperty(name="自定义", default=False, update=update_activate_customize)


    # MACHIN3pies

    activate_modes_pie: BoolProperty(name="模式 的饼菜单", default=True, update=update_activate_modes_pie)
    activate_save_pie: BoolProperty(name="保存 的饼菜单", default=True, update=update_activate_save_pie)
    activate_shading_pie: BoolProperty(name="着色 的饼菜单", default=True, update=update_activate_shading_pie)
    activate_views_pie: BoolProperty(name="视图 的饼菜单", default=True, update=update_activate_views_pie)
    activate_align_pie: BoolProperty(name="对齐 的饼菜单", default=True, update=update_activate_align_pie)
    activate_cursor_pie: BoolProperty(name="游标 的饼菜单", default=True, update=update_activate_cursor_pie)
    activate_workspace_pie: BoolProperty(name="工作区 的饼菜单", default=False, update=update_activate_workspace_pie)


    # MACHIN3menus
    activate_object_specials_menu: BoolProperty(name="物体特别菜单", default=True, update=update_activate_object_specials_menu)


    # hidden

    tabs: EnumProperty(name="Tabs", items=preferences_tabs, default="GENERAL")
    avoid_update: BoolProperty(default=False)
    dirty_keymaps: BoolProperty(default=False)



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
            self.draw_about(box)

    def draw_general(self, box):
        split = box.split()

        # LEFT

        b = split.box()
        b.label(text="触发")


        # MACHIN3tools

        bb = b.box()
        bb.label(text="工具")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_vert", toggle=True)
        row.label(text="智能顶点操作。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_edge", toggle=True)
        row.label(text="智能边缘创建，操作和转换选中项。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_face", toggle=True)
        row.label(text="智能平面创建和从面创建物体。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clean_up", toggle=True)
        row.label(text="快速几何清理。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clipping_toggle", toggle=True)
        row.label(text="视口裁剪平面切换。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_focus", toggle=True)
        row.label(text="与历史对象隔离。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mirror", toggle=True)
        row.label(text="物体镜像 + 非镜像。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align", toggle=True)
        row.label(text="物体每个轴的位置、旋转和比例对齐。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_customize", toggle=True)
        row.label(text="自定义各种 Blender 首选项，设置和键盘映射。")


        # MACHIN3pies

        bb = b.box()
        bb.label(text="饼菜单")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_modes_pie", toggle=True)
        row.label(text="快速模式更改。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_save_pie", toggle=True)
        row.label(text="保存，打开，追加。 加载最近，上一个和下一个。 追加世界环境和材质。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_shading_pie", toggle=True)
        row.label(text="控制着色，遮罩，eevee 和一些对象属性。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_views_pie", toggle=True)
        row.label(text="控制视图。 创建和管理相机。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align_pie", toggle=True)
        row.label(text="编辑栅格对齐。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_cursor_pie", toggle=True)
        row.label(text="游标相关。")

        row = column.split(factor=0.25)
        row.prop(self, "activate_workspace_pie", toggle=True)
        r = row.split(factor=0.4)
        r.label(text="切换工作区。")
        r.label(text="如果启用，请在 ui/pies.py 中对其进行自定义", icon="INFO")


        # MACHIN3menus

        bb = b.box()
        bb.label(text="菜单")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_object_specials_menu", toggle=True)
        row.label(text="物体特殊，访问工具，没有键盘映射。")


        # RIGHT

        b = split.box()
        b.label(text="设置")


        if getattr(bpy.types, "MACHIN3_OT_customize", False):
            bb = b.box()
            bb.label(text="自定义")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()
            row.prop(self, "custom_theme")
            row.prop(self, "custom_matcaps")
            row.prop(self, "custom_overlays")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()

            col = row.column()
            col.prop(self, "custom_preferences_interface")
            col.prop(self, "custom_preferences_viewport")

            col = row.column()
            col.prop(self, "custom_preferences_navigation")
            col.prop(self, "custom_preferences_keymap")

            col = row.column()
            col.prop(self, "custom_preferences_system")
            col.prop(self, "custom_preferences_save")

            if self.dirty_keymaps:
                row = column.row()
                row.label(text="键盘映射已被修改，需要先恢复它们。", icon="ERROR")
                row.operator("machin3.restore_keymaps", text="立刻恢复")
                row.label()

            column = bb.column()
            row = column.row()

            row.label()
            row.operator("machin3.customize")
            row.label()


        # MODES PIE

        if getattr(bpy.types, "MACHIN3_MT_modes_pie", False):
            bb = b.box()
            bb.label(text="模式 的饼菜单")

            column = bb.column()

            column.prop(self, "toggle_cavity")


        # SAVE PIE

        if getattr(bpy.types, "MACHIN3_MT_save_pie", False):
            bb = b.box()
            bb.label(text="保存 的饼菜单：追加世界环境和材质")

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
            c.operator("machin3.clear_appendmats", text="", icon='LOOP_BACK')
            c.operator("machin3.remove_appendmat", text="", icon_value=get_icon('cancel'))
            c.separator()
            c.operator("machin3.populate_appendmats", text="", icon='MATERIAL')
            c.operator("machin3.rename_appendmat", text="", icon='OUTLINER_DATA_FONT')


            row = column.row()
            row.prop(self, "appendmatsname")
            row.operator("machin3.add_separator", text="", icon_value=get_icon('separator'))


        # SHADING PIE

        if getattr(bpy.types, "MACHIN3_MT_shading_pie", False):
            bb = b.box()
            bb.label(text="着色 的饼菜单：材质捕获开关")

            column = bb.column()

            row = column.row()

            row.prop(self, "switchmatcap1")
            row.prop(self, "switchmatcap2")


        # NO SETTINGS

        if not any([getattr(bpy.types, "MACHIN3_" + name, False) for name in ["MT_modes_pie", "MT_save_pie", "MT_shading_pie"]]):
            b.label(text="没有工具或已激活带有设置的饼图菜单。")

    def draw_keymaps(self, box):
        wm = bpy.context.window_manager
        # kc = wm.keyconfigs.addon
        kc = wm.keyconfigs.user

        from . keys import keys

        split = box.split()

        b = split.box()
        b.label(text="Tools")

        if not self.draw_tool_keymaps(kc, keys, b):
            b.label(text="没有可用的键盘映射，因为没有激活任何工具。")


        b = split.box()
        b.label(text="饼菜单")

        if not self.draw_pie_keymaps(kc, keys, b):
            b.label(text="没有创建键盘映射，因为没有激活馅饼。")

    def draw_about(self, box):
        column = box.column()

        for idx, (text, url, icon) in enumerate(links):
            if idx % 2 == 0:
                row = column.row()
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url
            else:
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url

    def draw_tool_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" not in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_pie_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_keymap_items(self, kc, name, keylist, layout):
        drawn = False

        for idx, item in enumerate(keylist):
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
                    if len(keylist) == 1:
                        label = name.title().replace("_", " ")

                    # multi kmi tools, get it from the label tag, while the title is printed once, before the first item
                    else:
                        if idx == 0:
                            box.label(text=name.title().replace("_", " "))

                        label = item.get("label")

                    row = box.split(factor=0.15)
                    row.label(text=label)

                    # layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)

                    drawn = True
        return drawn
