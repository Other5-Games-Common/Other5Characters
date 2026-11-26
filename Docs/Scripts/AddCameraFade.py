# Lets the playable characters' materials fade out as the camera closes in on them (Other5's camera fade,
# Source/Other5/Public/Other5CameraFade.h): Other5StandIns.AddCameraFade (Other5Licensed) on every base material of the
# meshes below. Bring in does the same to the Countess and Gideon as it brings them in (StandIns.json "Fixups"), so run
# this only for a project that brought them in before that, or after adding a mesh here. Brought-in materials are copied
# back to the Other5 library too, so Bring in and Clean up still see them as the library's. Rerunnable:
#   UnrealEditor-Cmd Other5.uproject -run=pythonscript -script="<this file>"
import filecmp
import os
import shutil
import unreal
import Other5StandIns

MESHES = [
    "/Other5Characters/Mannequin/Meshes/SKM_Manny",
    "/Other5Characters/Mannequin/Meshes/SKM_Quinn",
    "/Other5Characters/Countess/Characters/Heroes/Countess/Meshes/SM_Countess",
    "/Other5Characters/Gideon/Characters/Heroes/Gideon/Meshes/Gideon",
]
PREFIX = "/Other5Characters/"


def log(s):
    unreal.log_warning("AddCameraFade: " + s)


def library():
    # As Other5Setup::LibraryDir: OTHER5_LIBRARY, else Other5Library next to the project folder (a LibraryDir set in
    # the Other5 Setup window isn't read here).
    env = os.environ.get("OTHER5_LIBRARY")
    if env:
        return env
    project = os.path.abspath(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()))
    return os.path.join(os.path.dirname(project.rstrip("/\\")), "Other5Library")


plugin_content = os.path.join(Other5StandIns.PluginDir("Other5Characters"), "Content")
lib_content = os.path.join(library(), "Other5Characters", "Content")
changed = synced = 0
done = set()
for path in MESHES:
    mesh = unreal.load_asset(path)
    if mesh is None:
        log("MISSING " + path)
        continue
    for slot in mesh.get_editor_property("materials"):
        mi = slot.get_editor_property("material_interface")
        base = mi.get_base_material() if mi else None
        if base is None or base.get_path_name() in done or not base.get_path_name().startswith(PREFIX):
            continue
        done.add(base.get_path_name())
        changed += Other5StandIns.AddCameraFade(base)
        rel = base.get_path_name().split(".")[0][len(PREFIX):] + ".uasset"
        mine, theirs = os.path.join(plugin_content, rel), os.path.join(lib_content, rel)
        if os.path.exists(theirs) and os.path.exists(mine) and not filecmp.cmp(mine, theirs, shallow=False):
            shutil.copyfile(mine, theirs)
            synced += 1
log("END %d materials, %d changed, %d copied to the library (%s)" % (len(done), changed, synced, lib_content))
