# RAIL Wichelsee — visual refinement v2

Reference-based visual approximation, 3 October 2026. This is a meaningful detail/material pass on the first checkpoint, not an exact OEM reconstruction or measured engineering model. Checkpoint 01 is preserved separately.

## Deliverables

- `RAIL_Wichelsee_visual_v2.glb`: self-contained glTF 2.0 model with embedded PBR maps, no external resources or required compression decoder.
- `RAIL_Wichelsee_visual_v2.blend`: Blender 4.3.2 editable source with 319 independently named mesh objects and packed 1024px master textures.
- `01_drivetrain_side_v2.png`, `02_opposite_side_v2.png`, `03_front_v2.png`, `04_rear_v2.png`, `05_three_quarter_v2.png`: neutral studio images rendered from a clean import of the exact delivered GLB.
- `06_photo_and_checkpoint_comparison_v2.png`: primary-photo and checkpoint comparison at matched wheel scale.
- `07_exported_detail_inspection_v2.png`: close-up geometry and material evidence from the same GLB.
- Model statistics, PBR master maps, build scripts and a portable local Three.js viewer are included in this archive.

## What changed in geometry

- Wheels: rounded tire cross-section; black crown/shoulders/beads with narrow tan sidewalls; fine shallow directional gravel tread; shaped satin rims; 28 thin double-butted two-cross spokes per wheel; nipples, hub tapers, flanges, axle caps and valves.
- Crank and cassette: substantial dark asymmetric four-arm spider and crank, machined tooth edges, visible fasteners, compact clipless pedals; 11 stepped flat toothed cassette sprockets with open cutouts. Counts and exact component engineering remain inferred.
- Chain and rear mech: 114 alternating plate-link segments with rollers/rivets on a closed tangent path; actual pulley wraps; angular derailleur body; two open cage plates and two detailed pulleys. This is static visual geometry, not a mechanically simulated transmission.
- Brakes: thin flat slotted rotors, carriers and calipers with mounting hardware. Real drivetrain/non-drivetrain asymmetry is retained.
- Bag: a curved, slightly bulged textile shell with restrained geometric wrinkles, seams, zipper tape/teeth/pulls and four top-tube plus two seat-tube straps. It is no longer a rigid wedge slab.
- Accessories: continuous cage backbones and frame-connected mounts; mini-pump saddles; rounded saddle with black rails; broader curved hood shells and thin brake blades; photo-supported small RAIL/KING/WHISKY/GRX cues.

## PBR materials and web size

The web GLB contains 12 embedded 512×512 PNG images: standard base-color, normal and roughness/metallic data for nylon, rubber, brown tape and sage paint. The editable project keeps the 1024px master maps, which are also supplied separately. Tangent normals use the OpenGL/glTF +Y convention. Base color is sRGB; roughness/normal data is linear. UVs repeat to represent small physical surface tiles rather than one stretched full-frame texture.

No studio lighting, photographic texture planes, rock, gradient or shadows are baked into the bicycle. The .blend studio is a separate collection, excluded from GLB. Set up environment illumination, lights, ground and dynamic shadows in the website scene. Metals benefit from a neutral environment map; a black scene without environment/reflection light will make them dark. The included viewer uses a neutral procedural studio environment and soft directional light as a starting point, not a prescribed final brand scene.

Web GLB: 146,224 triangles, 24 logical meshes, 52 material primitives/potential draw calls, 27 nodes and 12 materials. File size 8,455, 240 bytes (8.46MB decimal /8.06MiB). This is larger than checkpoint 01 because it contains real tread, chain/link mechanics and embedded surface textures. It was reduced from 11.42MB by using 512px web maps while retaining 1024px masters. Mobile memory/FPS and the target RAIL scroll behavior still need testing in the actual application.

## Scale and axes

All geometry is in meters. Tire outside diameter is assumed 0.714m; wheelbase inferred from the photo is 1.048m. Origin is at ground level below the midpoint between wheel axles. The exact exported bounding box is approximately 1.762m long ×1.002m high ×0.4964m wide. Wheel contact minimum is exactly0.

- Blender: +X forward, +Z up, drivetrain -Y.
- GLB/Three.js: +X forward, +Y up, drivetrain +Z.
- Front/rear wheel pivots are x ±0.524m and height 0.357m; their child wheel transforms are identity. Whole-bike rotation requires no special setup.
- Wheel-spinning animation is not authored. Rotors are separately named so an integrator can parent them to the corresponding wheel if needed; calipers should stay static.
- The frame/axle silhouette remains registered to the primary photo. Wheelbase/wheel diameter is about 1.47, and BB location is about 0.59 wheel diameters ahead of the rear axle.

## Validation performed

The exact final GLB was parsed as valid glTF 2.0, then reimported after deleting all source bicycle geometry from the inspection scene. All five delivery views and detail views were rendered from that reimport. Geometry attributes and UVs are finite; indices are in range; all 12 embedded PNGs are valid and 512×512; textured primitives have the required UV channels; no external URI or required extension remains. Exact wheel pivot centering and zero ground contact were checked.

A separate browser attempt could not open the cloud machine's localhost viewer because the browser blocked the address. Therefore v2 browser runtime/FPS is not claimed. The user's confirmation that checkpoint 01 rotated in RAIL V3 does not validate this new version. The included local viewer can be opened through a local HTTP server for a direct Three.js check. No website was deployed or project repository changed during this asset pass.

## Local viewer

From this extracted archive folder, run `python -m http.server 8765` (or use your normal static dev server), then open `http://localhost:8765/viewer/`. The viewer includes local Three.js modules and reads the GLB one directory above it. It offers both sides/front/rear/three-quarter views and an orbit/rotation control. The viewer's Three.js MIT license is included. Treat this as a testing aid, not a replacement for testing in RAIL V3.

## Still not confirmable from the references

No new measurements were supplied. Exact tire size/pressure/profile, frame size/geometry, bar width/reach/drop, bag dimensions, paint/fabric color calibration, hub spacing, hidden-side cable routing, saddle underside, fork cross-sections, precise drivetrain models/tooth counts, spoke pattern and brake details remain approximations. Visible product names were used only where readable; no claim of manufacturer CAD accuracy is made.

The most useful future inputs remain measured tire OD/width, wheelbase, handlebar hood/drop width, frame geometry/size and bag width; straight opposite-side/front/rear and front/rear three-quarter photographs of this same build, plus mechanical close-ups. This pass proceeds using the existing photos as requested; these gaps are documented rather than treated as a blocker.

## Source and scripts

The .blend is the main editable source and has all used texture images packed. Scripts reproduce the approximate geometry and material setup; Blender 4.3+ is expected. The build script uses a standard fallback font when DejaVu is not installed. Additional view/render scripts record the original validation workflow; adapt any local directory settings as needed. These assets use ordinary meshes and PBR data, with no image-card bicycle geometry.
