# Adds a Paragon hero (or any humanoid character pack imported with the Fab panel) to Other5Characters as a
# retargeted skin, the way the Countess and Gideon were added. Rerunnable; each step skips what's already done.
#
#   1. Move: the hero's mesh and everything it needs (materials, textures, skeleton, physics asset) from the Fab
#      import folder into /Other5Characters/<Hero>, keeping their relative paths. Animations, audio and FX stay
#      behind: Other5 plays the mannequin's animations on the hero through the retargeter.
#   2. IK_<Hero>: an IK Rig on the hero's mesh with the auto-generated retarget chains (spine, neck, head, arms,
#      legs, fingers) and the pelvis as retarget root, the same set IK_Countess has.
#   3. RTG_Mannequin_<Hero>: an IK Retargeter from IK_LyraMannequin (the mannequin every Other5 character runs on)
#      to IK_<Hero>, chains auto-mapped by name.
#
# Edit the settings below, then in the editor's console:  py "<this file>"
import unreal

HERO = "Gideon"
IMPORT_ROOT = "/Game/ParagonGideon"                                       # where the Fab panel put the pack
MESHES = ["/Game/ParagonGideon/Characters/Heroes/Gideon/Meshes/Gideon"]   # the looks to bring across
DEST_ROOT = "/Other5Characters/" + HERO
RIGS = DEST_ROOT + "/Rigs"
SOURCE_RIG = "/Other5Characters/Countess/Rigs/IK_LyraMannequin"

R = unreal.AssetRegistryHelpers.get_asset_registry()
Lib = unreal.EditorAssetLibrary
Tools = unreal.AssetToolsHelpers.get_asset_tools()

def log(s):
	unreal.log("AddParagonHero: " + s)

def closure(pkg, seen):
	if pkg in seen or not pkg.startswith(IMPORT_ROOT + "/"):
		return
	seen.add(pkg)
	opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=False, include_hard_package_references=True,
		include_searchable_names=False, include_soft_management_references=False, include_hard_management_references=False)
	for d in R.get_dependencies(pkg, opts) or []:
		closure(str(d), seen)

def moved(pkg):
	return DEST_ROOT + pkg[len(IMPORT_ROOT):]

# ---- 1. Move
todo = set()
for m in MESHES:
	if Lib.does_asset_exist(m):
		closure(m, todo)
		mesh = unreal.load_asset(m)
		for extra in (mesh.get_editor_property("skeleton"), mesh.get_editor_property("physics_asset")):
			if extra:
				closure(extra.get_outermost().get_name(), todo)
renames = []
for pkg in sorted(todo):
	asset = unreal.load_asset(pkg)
	if not asset:
		continue
	dest = moved(pkg)
	renames.append(unreal.AssetRenameData(asset, dest.rsplit("/", 1)[0], dest.rsplit("/", 1)[1]))
if renames:
	log("moving %d packages into %s" % (len(renames), DEST_ROOT))
	Tools.rename_assets(renames)
	for a in renames:
		Lib.save_loaded_asset(a.get_editor_property("asset"), False)
else:
	log("nothing left to move")
# Leave no redirectors behind in the import folder.
reds = [a.get_asset() for a in R.get_assets(unreal.ARFilter(package_paths=[IMPORT_ROOT], recursive_paths=True,
	class_paths=[unreal.TopLevelAssetPath("/Script/CoreUObject", "ObjectRedirector")]))]
if reds:
	fix = getattr(Tools, "fixup_referencers", None) or getattr(unreal.AssetToolsHelpers.get_asset_tools(), "fix_up_redirectors", None)
	if fix:
		fix(reds)
		log("fixed up %d redirectors" % len(reds))
	else:
		log("redirectors left (Fix Up Redirectors on %s by hand): %d" % (IMPORT_ROOT, len(reds)))

mesh = unreal.load_asset(moved(MESHES[0]))
if not mesh:
	raise RuntimeError("AddParagonHero: no mesh at " + moved(MESHES[0]))

# ---- 2. IK Rig
rig_path = RIGS + "/IK_" + HERO
rig = unreal.load_asset(rig_path)
if not rig:
	rig = Tools.create_asset("IK_" + HERO, RIGS, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
	c = unreal.IKRigController.get_controller(rig)
	c.set_skeletal_mesh(mesh)
	c.apply_auto_generated_retarget_definition()
	c.apply_auto_fbik()
	c.set_retarget_root("pelvis")
	Lib.save_loaded_asset(rig, False)
	log("made " + rig_path)
c = unreal.IKRigController.get_controller(rig)
log("IK_%s chains: %s" % (HERO, ", ".join(str(ch.get_editor_property("chain_name")) for ch in c.get_retarget_chains())))

# ---- 3. IK Retargeter
rtg_path = RIGS + "/RTG_Mannequin_" + HERO
rtg = unreal.load_asset(rtg_path)
if not rtg:
	rtg = Tools.create_asset("RTG_Mannequin_" + HERO, RIGS, unreal.IKRetargeter, unreal.IKRetargetFactory())
	rc = unreal.IKRetargeterController.get_controller(rtg)
	rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, unreal.load_asset(SOURCE_RIG))
	rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, rig)
	if rc.get_num_retarget_ops() == 0:
		rc.add_default_ops()
	rc.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, rig)
	rc.auto_map_chains(unreal.AutoMapChainType.EXACT, True)
	rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET, mesh)
	Lib.save_loaded_asset(rtg, False)
	log("made " + rtg_path)
log("done")
