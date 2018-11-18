
classes = {"CORE": [("ui.UILists", [("AppendMatsUIList", "")]),
                    ("properties", [("AppendMatsCollection", "")]),
                    ("preferences", [("MACHIN3toolsPreferences", "")]),
                    ("properties", [("HistoryObjectsCollection", ""), ("HistoryUnmirroredCollection", ""), ("HistoryEpochCollection", ""), ("M3SceneProperties", "")])],

           "SMART_VERT": [("operators.smart_vert", [("SmartVert", "smart_vert")])],
           "SMART_EDGE": [("operators.smart_edge", [("SmartEdge", "smart_edge")])],
           "SMART_FACE": [("operators.smart_face", [("SmartFace", "smart_face")])],
           "CLEAN_UP": [("operators.clean_up", [("CleanUp", "clean_up")])],
           "CLIPPING_TOGGLE": [("operators.clipping_toggle", [("ClippingToggle", "clipping_toggle")])],
           "FOCUS": [("operators.focus", [("Focus", "focus")])],
           "MIRROR": [("operators.mirror", [("Mirror", "mirror")])],
           "ALIGN": [("operators.align", [("Align", "align")])],

           "MODES_PIE": [("ui.pies", [("PieModes", "modes_pie")]),
                         ("ui.operators.modes", [("EditMode", "edit_mode"), ("VertexMode", "vertex_mode"), ("EdgeMode", "edge_mode"), ("FaceMode", "face_mode")])],

           "SAVE_PIE": [("ui.pies", [("PieSave", "save_pie")]),
                        ("ui.menus", [("MenuAppendMaterials", "append_materials")]),
                        ("ui.operators.save", [("New", "new"), ("Save", "save"), ("SaveIncremental", "save_incremental"), ("LoadMostRecent", "load_most_recent"), ("LoadPrevious", "load_previous"), ("LoadNext", "load_next")]),
                        ("ui.operators.save", [("AppendWorld", "append_world"), ("AppendMaterial", "append_material"), ("LoadWorldSource", "load_world_source"), ("LoadMaterialsSource", "load_materials_source")]),
                        ("ui.operators.appendmats", [("Add", "add_appendmat"), ("Move", "move_appendmat"), ("Rename", "rename_appendmat"), ("Clear", "clear_appendmats"), ("Remove", "remove_appendmat")])],


           "SHADING_PIE": [("ui.pies", [("PieShading", "shading_pie")]),
                           ("ui.operators.shading", [("ShadeSolid", "shade_solid"), ("ShadeMaterial", "shade_material"), ("ShadeRendered", "shade_rendered"), ("ShadeWire", "shade_wire")]),
                           ("ui.operators.toggle_grid_wire_outline", [("ToggleGrid", "toggle_grid"), ("ToggleWireframe", "toggle_wireframe"), ("ToggleOutline", "toggle_outline")]),
                           ("ui.operators.shade_smooth_flat", [("ShadeSmooth", "shade_smooth"), ("ShadeFlat", "shade_flat")]),
                           ("ui.operators.colorize_materials", [("ColorizeMaterials", "colorize_materials")]),
                           ("ui.operators.matcap_switch", [("MatcapSwitch", "matcap_switch")])],
           "VIEWS_PIE": [("ui.pies", [("PieViews", "views_pie")]),
                         ("ui.operators.views_and_cams", [("ViewAxis", "view_axis"), ("MakeCamActive", "make_cam_active"), ("SmartViewCam", "smart_view_cam")])],
           "ALIGN_PIE": [("ui.pies", [("PieAlign", "align_pie")]),
                         ("ui.operators.align", [("AlignEditMesh", "align_editmesh")])],
           "WORKSPACE_PIE": [("ui.pies", [("PieWorkspace", "workspace_pie")]),
                             ("ui.operators.switch_workspace", [("SwitchWorkspace", "switch_workspace")])],
           }
