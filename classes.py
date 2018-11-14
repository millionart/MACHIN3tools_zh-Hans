from . utils import MACHIN3 as m3


def get_classes(classes):
    classes = get_ui_classes(classes)

    classes = get_op_classes(classes)

    return classes


def get_ui_classes(classes):
    from . ui.pie import PieSelectMode, PieChangeShading, PieViewsAndCams, PieSaveOpenAppend, PieSwitchWorkspace
    from . ui.menu import MenuAppendMaterials
    from . ui.operators.select_mode import ToggleEditMode, SelectVertexMode, SelectEdgeMode, SelectFaceMode
    from . ui.operators.change_shading import ShadeSolid, ShadeMaterial, ShadeRendered
    from . ui.operators.toggle_grid_wire_outline import ToggleGrid, ToggleWireframe, ToggleOutline
    from . ui.operators.shade_smooth_flat import ShadeSmooth, ShadeFlat
    from . ui.operators.colorize_materials import ColorizeMaterials
    from . ui.operators.matcap_switch import MatcapSwitch
    from . ui.operators.views_and_cams import ViewAxis, MakeCamActive, SmartViewCam
    from . ui.operators.save_load_append import New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext
    from . ui.operators.save_load_append import AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource
    from . ui.operators.appendmats import Add, Move, Rename, Clear, Remove
    from . ui.operators.switch_workspace import SwitchWorkspace

    # SELECT MODE
    classes.append(PieSelectMode)
    classes.extend([SelectVertexMode, SelectEdgeMode, SelectFaceMode, ToggleEditMode])

    # CHANGE SHADING
    classes.append(PieChangeShading)
    classes.extend([ShadeSolid, ShadeMaterial, ShadeRendered])
    classes.extend([ToggleGrid, ToggleWireframe, ToggleOutline])
    classes.extend([ShadeSmooth, ShadeFlat])
    classes.extend([ColorizeMaterials, MatcapSwitch])

    # VIEWS and CAMS
    classes.append(PieViewsAndCams)
    classes.extend([ViewAxis, MakeCamActive, SmartViewCam])

    # SAVE, OPEN, Append
    classes.append(PieSaveOpenAppend)
    classes.append(MenuAppendMaterials)
    classes.extend([New, Save, SaveIncremental, LoadMostRecent, LoadPrevious, LoadNext])
    classes.extend([AppendWorld, AppendMaterial, LoadWorldSource, LoadMaterialsSource])
    classes.extend([Add, Move, Rename, Clear, Remove])

    # SWITCH WORKSPACE
    classes.append(PieSwitchWorkspace)
    classes.append(SwitchWorkspace)

    return classes


def get_op_classes(classes):
    from . operators.smart_vert import SmartVert
    from . operators.smart_edge import SmartEdge
    from . operators.smart_face import SmartFace

    from . operators.clean_up import CleanUp
    from . operators.clipping_toggle import ClippingToggle
    from . operators.focus import Focus
    from . operators.mirror import Mirror
    from . operators.align import Align

    # SMART VERT
    classes.append(SmartVert)

    # SMART EDGE
    classes.append(SmartEdge)

    # SMART EDGE
    classes.append(SmartFace)

    # CLEAN UP
    classes.append(CleanUp)

    # CLIPPING TOGGLE
    classes.append(ClippingToggle)

    # FOCUS
    classes.append(Focus)

    # MIRROR
    classes.append(Mirror)

    # ALIGN
    classes.append(Align)


    return classes
