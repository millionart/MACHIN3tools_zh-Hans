import os
import bpy
import bpy.utils.previews

iconsCOL = None
path = os.path.dirname(__file__)


def get_icon(name):
    return iconsCOL[name].icon_id


def register_icons():
    global iconsCOL
    iconsCOL = bpy.utils.previews.new()

    for i in sorted(os.listdir(path)):
        if i.endswith(".png"):
            iconname = i[:-4]
            filepath = os.path.join(path, i)

            iconsCOL.load(iconname, filepath, 'IMAGE')


def unregister_icons():
    bpy.utils.previews.remove(iconsCOL)
