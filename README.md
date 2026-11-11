# Other5Characters

Playable character art for Other5 Creations, content only: Manny and Quinn (meshes, skeleton, animations, rigs), the
Countess, and the animation compression settings every creation animation uses (`Other5AnimBoneCompressionSettings`,
`Other5AnimCurveCompressionSettings`). Other5Combat and Other5Creatures need it.

## What's real here, and what's a stand-in
- **Real, from Unreal Engine's own templates** (Epic lets anyone share these): the mannequin skeleton, the Manny and
  Quinn meshes, their materials and textures, the control rigs and physics asset, and about 100 animations (unarmed,
  pistol and rifle locomotion, aim offsets, fire, reload, equip, hit reacts, deaths). They sit at the paths Other5's
  Blueprints use; the rest of the template pack is under `Template/`.
- **Stand-ins** for what comes from Lyra and Paragon (Epic's licence doesn't let anyone share those source files):
  - the rest of the Lyra animations, each a copy of the nearest template animation, so characters still move;
  - Lyra's animation Blueprints, copies of the template's `ABP_Unarmed`;
  - the Countess, a magenta-checked mannequin.

  `StandIns.json` lists each one and where the real asset comes from.

To get the real look, use **Tools > Other5 Setup** in the Other5 Creator. It walks you through getting Lyra Starter
Game and Paragon: Countess from Fab with your own Epic account (both free), then puts the real assets in place of the
stand-ins. Your Creation's paks then ship them, cooked, under your own licence. The real files live in your **Other5
library** (by default a folder `Other5Library` next to your project folder), never in this repository.

## Using it
- Manny and Quinn: `Mannequin/Meshes/SKM_Manny`, `SKM_Quinn`, skeleton `Mannequin/Meshes/SK_Mannequin`.
- A character of your own: import its mesh and animations into your Creation, set every animation's Bone and Curve
  Compression Settings to the two assets above, and add an IK Retargeter to play the mannequin animations on it.
