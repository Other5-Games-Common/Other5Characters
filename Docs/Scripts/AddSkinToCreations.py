# Adds a character skin to the player characters of Other5's Creations: one more entry in the Skins list of each
# Blueprint's Other5CharacterSkins component (the same thing as clicking + on Skins in the Details panel).
# Rerunnable: a Blueprint that already has a skin with that name gets it updated in place.
#
# Edit SKIN and BLUEPRINTS, then in the editor's console:  py "<this file>"
import unreal

SKIN = {
	"name": "Gideon",
	"mesh": None,                                                                  # same skeleton as the mannequin? its mesh
	"retargeted_mesh": "/Other5Characters/Gideon/Characters/Heroes/Gideon/Meshes/Gideon",  # other skeleton: shown instead
	"retargeter": "/Other5Characters/Gideon/Rigs/RTG_Mannequin_Gideon",
	"hidden_material_slots": [],                                                   # props built into the mesh, e.g. swords
	"toughness": 2.5, "speed": 0.0, "accuracy": 2.5,                               # fighter stats it starts with, percent
}
BLUEPRINTS = [
	"/CubeEscape/Blueprints/BP_CubePlayerCharacter",
	"/SKIvSKI/Blueprints/BP_SkiCharacter",
]

Sub = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
SubLib = unreal.SubobjectDataBlueprintFunctionLibrary

def log(s):
	unreal.log("AddSkinToCreations: " + s)

def skins_component(bp):
	for h in Sub.k2_gather_subobject_data_for_blueprint(bp):
		o = SubLib.get_object(SubLib.get_data(h))
		if isinstance(o, unreal.Other5CharacterSkins):
			return o
	return None

def make_skin():
	s = unreal.Other5CharacterSkin()
	s.set_editor_property("display_name", unreal.Text(SKIN["name"]))
	if SKIN["mesh"]:
		s.set_editor_property("mesh", unreal.load_asset(SKIN["mesh"]))
	if SKIN["retargeted_mesh"]:
		s.set_editor_property("retargeted_mesh", unreal.load_asset(SKIN["retargeted_mesh"]))
		s.set_editor_property("retargeter", unreal.load_asset(SKIN["retargeter"]))
	s.set_editor_property("hidden_material_slots", [unreal.Name(n) for n in SKIN["hidden_material_slots"]])
	for stat in ("toughness", "speed", "accuracy"):
		s.set_editor_property(stat, SKIN[stat])
	return s

for path in BLUEPRINTS:
	bp = unreal.load_asset(path)
	if not bp:
		log("skipped (not found): " + path)
		continue
	comp = skins_component(bp)
	if not comp:
		log("skipped (no Other5CharacterSkins): " + path)
		continue
	skins = list(comp.get_editor_property("skins"))
	names = [str(s.get_editor_property("display_name")) for s in skins]
	if SKIN["name"] in names:
		skins[names.index(SKIN["name"])] = make_skin()
		log("%s: updated %s" % (path, SKIN["name"]))
	else:
		skins.append(make_skin())
		log("%s: added %s as skin %d" % (path, SKIN["name"], len(skins)))
	comp.set_editor_property("skins", skins)
	unreal.BlueprintEditorLibrary.compile_blueprint(bp)
	unreal.EditorAssetLibrary.save_loaded_asset(bp, False)
	log("%s skins: %s" % (path, [str(s.get_editor_property("display_name")) for s in skins]))
