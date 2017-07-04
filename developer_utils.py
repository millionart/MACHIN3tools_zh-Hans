import os
import pkgutil
import importlib
import rna_keymap_ui


def setup_addon_modules(path, package_name, reload):
    """
    Imports and reloads all modules in this addon.

    path -- __path__ from __init__.py
    package_name -- __name__ from __init__.py
    """
    def get_submodule_names(path=path[0], root=""):
        module_names = []
        for importer, module_name, is_package in pkgutil.iter_modules([path]):
            if is_package:
                sub_path = os.path.join(path, module_name)
                sub_root = root + module_name + "."
                module_names.extend(get_submodule_names(sub_path, sub_root))
            else:
                module_names.append(root + module_name)
        return module_names

    def import_submodules(names):
        modules = []
        for name in names:
            modules.append(importlib.import_module("." + name, package_name))
        return modules

    def reload_modules(modules):
        for module in modules:
            importlib.reload(module)

    names = get_submodule_names()
    modules = import_submodules(names)
    if reload:
        reload_modules(modules)
    return modules


def get_keymap_item(km, kmi_name, kmi_value, properties):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if properties == 'name':
                if km.keymap_items[i].properties.name == kmi_value:
                    return km_item
            elif properties == 'tab':
                if km.keymap_items[i].properties.tab == kmi_value:
                    return km_item
            elif properties == 'none':
                return km_item
    return None


def show_keymap(condition, kc, keymap, addon, col):
    km = kc.keymaps[keymap]
    if condition:
        try:
            kmi = get_keymap_item(km, addon, 'none', 'none')
            kmi.active = True
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        except:
            pass
    else:
        try:
            kmi = get_keymap_item(km, addon, 'none', 'none')
            kmi.active = False
        except:
            pass
