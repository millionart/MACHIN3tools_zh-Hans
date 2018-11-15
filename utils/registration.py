from bpy.utils import register_class, unregister_class
from . import MACHIN3 as m3


def register_classes(classes):
    for c in classes:
        register_class(c)

    return classes


def unregister_classes(classes):
    for c in classes:
        unregister_class(c)



def get_core_classes():
    from .. preferences import MACHIN3toolsPreferences
    from .. properties import AppendMatsCollection, M3SceneProperties, HistoryEpochCollection, HistoryObjectsCollection, HistoryUnmirroredCollection
    from .. ui.UILists import AppendMatsUIList

    classes = []

    # PREFERENCES
    classes.extend([AppendMatsUIList, AppendMatsCollection, MACHIN3toolsPreferences])

    # PROPERTIES
    classes.extend([HistoryObjectsCollection, HistoryUnmirroredCollection, HistoryEpochCollection, M3SceneProperties])

    return classes


def get_ui_classes():
    classes = []


    # MODES

    if m3.M3_prefs().activate_pie_modes:
        from .. ui.pie import PieModes
        from .. ui.operators.select_mode import ToggleEditMode, SelectVertexMode, SelectEdgeMode, SelectFaceMode

        classes.append(PieModes)
        classes.extend([SelectVertexMode, SelectEdgeMode, SelectFaceMode, ToggleEditMode])


    # SAVE

    if m3.M3_prefs().activate_pie_save:
        from .. ui.pie import PieSave
        from .. ui.menu import MenuAppendMaterials
        from .. ui.operators.save_load_append import New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext
        from .. ui.operators.save_load_append import AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource
        from .. ui.operators.appendmats import Add, Move, Rename, Clear, Remove

        classes.append(PieSave)
        classes.append(MenuAppendMaterials)
        classes.extend([New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext])
        classes.extend([AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource])
        classes.extend([Add, Move, Rename, Clear, Remove])


    # SHADING

    if m3.M3_prefs().activate_pie_shading:
        from .. ui.pie import PieShading
        from .. ui.operators.change_shading import ShadeSolid, ShadeMaterial, ShadeRendered
        from .. ui.operators.toggle_grid_wire_outline import ToggleGrid, ToggleWireframe, ToggleOutline
        from .. ui.operators.shade_smooth_flat import ShadeSmooth, ShadeFlat
        from .. ui.operators.colorize_materials import ColorizeMaterials
        from .. ui.operators.matcap_switch import MatcapSwitch

        classes.append(PieShading)
        classes.extend([ShadeSolid, ShadeMaterial, ShadeRendered])
        classes.extend([ToggleGrid, ToggleWireframe, ToggleOutline])
        classes.extend([ShadeSmooth, ShadeFlat])
        classes.extend([ColorizeMaterials, MatcapSwitch])


    # VIEWS

    if m3.M3_prefs().activate_pie_views:
        from .. ui.pie import PieViews
        from .. ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam

        classes.append(PieViews)
        classes.extend([ViewAxis, MakeCamActive, SmartViewCam])


    # SWITCH WORKSPACE

    if m3.M3_prefs().activate_pie_workspace:
        from .. ui.pie import PieWorkspace
        from .. ui.operators.switch_workspace import SwitchWorkspace

        classes.append(PieWorkspace)
        classes.append(SwitchWorkspace)

    return classes


def get_op_classes():
    classes = []

    # SMART VERT

    if m3.M3_prefs().activate_smart_vert:
        from .. operators.smart_vert import SmartVert

        classes.append(SmartVert)


    # SMART EDGE

    if m3.M3_prefs().activate_smart_edge:
        from .. operators.smart_edge import SmartEdge

        classes.append(SmartEdge)


    # SMART FACE

    if m3.M3_prefs().activate_smart_face:
        from .. operators.smart_face import SmartFace

        classes.append(SmartFace)


    # CLEAN UP

    if m3.M3_prefs().activate_clean_up:
        from .. operators.clean_up import CleanUp
        classes.append(CleanUp)


    # CLIPPING TOGGLE

    if m3.M3_prefs().activate_clipping_toggle:
        from .. operators.clipping_toggle import ClippingToggle
        classes.append(ClippingToggle)


    # FOCUS

    if m3.M3_prefs().activate_focus:
        from .. operators.focus import Focus
        classes.append(Focus)


    # MIRROR

    if m3.M3_prefs().activate_mirror:
        from .. operators.mirror import Mirror
        classes.append(Mirror)


    # ALIGN

    if m3.M3_prefs().activate_align:
        from .. operators.align import Align
        classes.append(Align)


    return classes
