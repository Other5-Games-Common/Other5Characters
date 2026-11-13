# Other5Characters: every animation must use Other5's compression settings (the Other5 Tool refuses to publish others,
# because the Other5 client only has these). The template animations came in with the engine's. Rerunnable.
import unreal
R = unreal.AssetRegistryHelpers.get_asset_registry()
R.search_all_assets(True)
Bone = unreal.load_asset("/Other5Characters/Other5AnimBoneCompressionSettings.Other5AnimBoneCompressionSettings")
Curve = unreal.load_asset("/Other5Characters/Other5AnimCurveCompressionSettings.Other5AnimCurveCompressionSettings")
Fixed = []
for D in R.get_assets_by_path("/Other5Characters", recursive=True):
	if str(D.asset_class_path.asset_name) != "AnimSequence":
		continue
	A = D.get_asset()
	if not A:
		continue
	if A.get_editor_property("bone_compression_settings") != Bone or A.get_editor_property("curve_compression_settings") != Curve:
		A.set_editor_property("bone_compression_settings", Bone)
		A.set_editor_property("curve_compression_settings", Curve)
		unreal.EditorAssetLibrary.save_loaded_asset(A, False)
		Fixed.append(str(D.package_name))

unreal.log("TemplateCompression: %d animation(s) now use Other5's compression settings" % len(Fixed))
