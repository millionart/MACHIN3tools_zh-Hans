import bpy
import os


def abspath(path):
    return os.path.abspath(bpy.path.abspath(path))


def quotepath(path):
    if " " in path:
        path = '"%s"' % (path)
    return path


def add_path_to_recent_files(path):
    """
    add the path to the recent files list, for some reason it's not done automatically when saving or loading
    """

    try:
        recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")
        with open(recent_path, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(path.rstrip('\r\n') + '\n' + content)

    except (IOError, OSError, FileNotFoundError):
        pass


def open_folder(path):
    import platform
    import subprocess

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        # subprocess.Popen(["xdg-open", path])
        os.system('xdg-open "%s" %s &' % (path, "> /dev/null 2> /dev/null"))  # > sends stdout,  2> sends stderr


def makedir(pathstring):
    if not os.path.exists(pathstring):
        os.makedirs(pathstring)
    return pathstring
