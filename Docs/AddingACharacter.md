# Add a new character to your Creation (worked example: Paragon: Gideon)

This guide follows one real addition, Paragon: Gideon, into the `Other5Characters` plugin and two Creations
(SKIvSKI and CubeEscape), on 2026-11-14. The same steps work for any humanoid character from Fab, or your own.
Screenshots (named in the steps) are in the project library.

## What you end up with
- The character in your project, animated by the mannequin animations every Other5 character already uses (no new
  Animation Blueprint), through an **IK Retargeter**.
- A **skin** entry on your player character's `Other5CharacterSkins` component, so players pick it in
  **Choose your fighter** and in Settings > Character. Its portrait is rendered in game; you don't make one.
- No C++. Every value (name, mesh, retargeter, hidden material slots, fighter stats) is set on the Blueprint.

## How Other5 does characters
Every Other5 player character runs on the UE mannequin skeleton (`SK_Mannequin`): its Animation Blueprints, weapons,
aim and hit reacts all assume it. A character on another skeleton, like a Paragon hero, is a **retargeted skin**: the
mannequin keeps animating, hidden, and the IK Retargeter copies its pose onto the visible hero mesh every frame. A
character already on the mannequin skeleton is simpler: it's a plain **Mesh** skin.

## Step 1: Get the character on Fab (you, with your own Epic account)
1. Open the listing ([Paragon: Gideon](https://www.fab.com/listings/51935254-f70f-400a-8ca5-91a3e1b83e3b)), sign in
   and read the licence. Gideon is free under the Fab Standard License; you may not use the PARAGON trademark to
   name or advertise your game.
2. Click **Add to My Library**. Nobody can do this for you: accepting a licence is your own agreement with Epic.

## Step 2: Import it with the editor's Fab panel
1. In the Other5 Creator: **Window > Fab**, sign in, open the listing (or **My Library**) and click **Add to Project**.
   *(screenshot 02-FabPanel.png)*
2. The pack lands in `Content/ParagonGideon`: about 2,000 files and 2 GB of source, with animations, voice lines, FX,
   four alternate skins and a sample character. You'll only keep what the character's mesh needs.
3. Using git? Add `/Content/ParagonGideon/` to `.gitignore` so the licensed files never get committed.

## Step 3: Check the character fits
Open the mesh (`Characters/Heroes/Gideon/Meshes/Gideon`) and look at:
- **Material slots.** Paragon meshes sometimes carry props as their own slots. Countess has swords
  (`M03_Swords_holster`), which her skin hides. Gideon has no weapons; his back ring is his portal (`M05_Portal_skin05`),
  part of his look, so nothing is hidden.
- **Skeleton.** Gideon uses his own `Gideon_Skeleton` (so he's a retargeted skin). All four alternate skins (Inquisitor,
  Mephisto, Tough, Undertow) share it and the same physics asset, so a variant only costs its own meshes and textures.

## Step 4: Move it into your plugin, and make the IK Rig and Retargeter
`Other5Characters/Docs/Scripts/AddParagonHero.py` does all three. Edit `HERO`, `IMPORT_ROOT` and `MESHES` at the top,
then type `py "<path>/AddParagonHero.py"` in the editor's console (Cmd box at the bottom). By hand, it's:
1. **Move** the mesh and everything it uses (materials, textures, skeleton, physics asset) into your plugin, here
   `Other5Characters/Gideon`, keeping the folder structure: find them with the mesh's **Reference Viewer** (or Size
   Map), drag them into the matching folders and pick **Move Here**. Then right-click the old folder > **Fix Up
   Redirectors**.
   Animations, audio and FX stay behind; Gideon plays the mannequin's animations. For Gideon that's 122 assets.
2. **IK Rig** (`Rigs/IK_Gideon`): right-click > Animation > Retargeting > IK Rig, pick the Gideon mesh, then
   **Auto Create Retarget Chains** and **Auto Create IK**. The retarget root is `pelvis`. You get the same 21 chains as
   Countess (spine, neck, head, arms, legs, fingers). *(screenshot 04-IKRig.png)*
3. **IK Retargeter** (`Rigs/RTG_Mannequin_Gideon`): source `IK_LyraMannequin` (in `Other5Characters/Countess/Rigs`),
   target `IK_Gideon`. Chains map by name. The output log should say the retargeter is ready to transfer animation
   from SKM_Manny to Gideon. Both are in A-pose, so the default retarget pose works. *(screenshot 05-Retargeter.png)*

## Step 5: Add the skin to your player character
On your player character Blueprint, select the **Other5CharacterSkins** component and add an element to **Skins**
(`AddSkinToCreations.py` does this for several Blueprints at once):

| Field | Gideon's value |
|---|---|
| Display Name | Gideon |
| Mesh | empty (Gideon isn't on the mannequin skeleton) |
| Retargeted Mesh | `Other5Characters/Gideon/Characters/Heroes/Gideon/Meshes/Gideon` |
| Retargeter | `Other5Characters/Gideon/Rigs/RTG_Mannequin_Gideon` |
| Hidden Material Slots | none (Countess: `M03_Swords_holster`) |
| Toughness / Speed / Accuracy | 2.5 / 0 / 2.5 (fighter stats it starts with, in percent) |

Turn on **Choose On Join** and **Menu Button** for the character select screen. Choose your fighter shows every skin;
the Settings row shows up to four.

## Step 6: Test
Open a map (SKIvSKI: `L_SkiTest`) and press Play.
- If the editor asks whether to play with **GideonPlayerCharacter** failing to compile, click **Play in Editor**: that's
  the pack's old sample Blueprint (it uses UE4 input), and nothing of yours uses it. Deleting `Content/ParagonGideon`
  once you're done also removes it.
- Pick Gideon in Choose your fighter *(screenshot 08-ChooseYourFighter.png)*, then run, jump, aim, fire, reload, die.

## Step 7: Share your Creation
Cook and upload with the Other5 Tool as usual. Only what the skin references is cooked into your pak, under your own
licence.

## Size: what a character costs
Source sizes (uncooked) for Gideon: the default look needs about 430 MB, mostly 4K material-layer textures. Each extra
skin adds its own meshes and textures: Mephisto +75 MB, Tough +291 MB, Inquisitor +366 MB, Undertow +480 MB. Cooked
paks are smaller (compressed textures), and capping the textures' max size (2K or 1K) cuts them further.

## Publishing a public plugin (Other5's own repos)
Licensed files can't go to a public GitHub repo. Other5's public plugins hold **stand-ins** at the same paths, and the
real art lives in each machine's **Other5 library** (`F:\HomeDev\Other5Library`, beside the project). For Gideon:
1. Describe the licensed packages while the real ones are there (`Other5StandIns.Describe`, from
   `Plugins/Other5Licensed/Content/Python`).
2. Close the editor and move the real files into `Other5Library\Other5Characters\Content\Gideon`.
3. Make the stand-ins headless (`Other5StandIns.Create`, then `DropScratch`) and list them in the plugin's
   `StandIns.json` with `"Source": "Fab:ParagonGideon"`. The rigs stay real: they're Other5's own work.
4. Commit (here 123 small files, 1.3 MB), then `Other5Library.ps1 -Project <project> -Apply` puts the real art back
   locally, marked skip-worktree so git never sees it.
5. Add the source to `Plugins/Other5Licensed/Sources.json` so **Tools > Other5 Setup** can walk other Creators through
   getting Gideon themselves.

`Tests/CleanCreator/Make-PublicPlugin.ps1` does the same for a whole plugin in a clean Creator.
