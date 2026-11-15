# Countess's metal layer uses T_Blank_N, a flat normal map. The one from Paragon isn't in any Fab download any more, so
# Other5 makes its own at the same path: a 4x4 texture of the flat normal (128, 128, 255), Normalmap compression.
# Headless: UnrealEditor-Cmd.exe Other5.uproject -run=pythonscript -script="<this file>"
import os, struct, tempfile, zlib, unreal

PACKAGE = "/Other5Characters/Countess/Characters/Global/MaterialLayers/Metal/T_Blank_N"

def png(path, size, rgb):
	row = b"\x00" + bytes(rgb) * size
	raw = row * size
	def chunk(kind, data):
		return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
	with open(path, "wb") as f:
		f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
			+ chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

file = os.path.join(tempfile.mkdtemp(), "T_Blank_N.png")
png(file, 4, (128, 128, 255))
task = unreal.AssetImportTask()
for k, v in (("filename", file), ("destination_path", PACKAGE.rsplit("/", 1)[0]), ("destination_name", "T_Blank_N"),
		("automated", True), ("replace_existing", True), ("save", False)):
	task.set_editor_property(k, v)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
tex = unreal.load_asset(PACKAGE)
tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
tex.set_editor_property("srgb", False)
unreal.EditorAssetLibrary.save_loaded_asset(tex, False)
unreal.log("MakeBlankNormal: made " + PACKAGE)
