# RAIL Wichelsee — first 3D blockout checkpoint

Status: photo-informed blockout for proportion review, not an approved high-detail reconstruction. Created 3 October 2026. No website was changed or deployed.

## Included

- RAIL_Wichelsee_blockout.blend: editable Blender 4.3.2 source, 418 separate mesh objects with component/material names. Bicycle and studio live in separate collections.
- RAIL_Wichelsee_blockout.glb: genuine volumetric glTF 2.0, consolidated into 22 logical meshes and 42 material primitives (potential draw calls), 25 nodes, 47,984 triangles. Ten PBR materials, no texture images or external resources. Geometry, not a photo cutout, billboard, or shallow extrusion.
- 01–05 PNG: drivetrain side, opposite side, front, rear and three-quarter. All are orthographic studio renders made after importing the exact deliverable GLB into a clean bicycle scene.
- 06_primary_photo_comparison.png: same-scale comparison with the primary photo, documented reference landmarks and approximate normalized ratios.
- 00_checkpoint_overview.png: compact visual overview.
- model_statistics.json and the reproducible Python build/validation scripts are included in the ZIP.

## Geometry and reference decisions

Read the complete WICHELSEE_3D_BRIEF.md and all four supplied reference images. The ZIP contains higher-resolution originals: primary 3266 × 4898 pixels, other images 4898 × 3265 or 3265 × 4898. The separately attached files are smaller versions. Used the ZIP originals for detail inspection and the green gravel build only. The other bicycles' suspension forks, flat bars, tires and rear suspension were not copied.

Primary 01 reference governs wheel spacing, frame junctions, tall seatpost, black rigid fork, compact brown drop bars, shallow wedge-shaped frame bag, single front chainring and forward/upward drive crank. Additional views informed separate fork legs, flared bar width, bag thickness and side asymmetry. Two silver wire cages and the black mini-pump are geometrically separate. Bag folds, exact drivetrain hardware, cable routing and saddle undersides are deliberately simplified. Tire volume is modeled, but fine gravel tread and decals await the detailed pass.

Independent shape review led to a shallower bag, reduced cassette size, deeper sage/brown/tan color values, softened saddle nose and removal of a distracting ground edge. These materials are initial physically based estimates, not calibrated paint or fabric matches.

## Scale, origin and orientation

Scale is provisional. Assumed outside tire diameter: 0.714 m; measured image wheel diameter approximately 352 pixels at 1366 px-wide analysis size. This fixes the scale, rather than proving the real size. Wheelbase inferred from approximately 516 pixels: 1.048 m. Normalized wheelbase is about 1.47 diameters; bottom bracket position is approximately 0.59 diameters ahead of rear axle. Other small discrepancies reflect photographic perspective, uncertain landmark placement and the equal-wheel, flat-ground reconstruction.

- Units: meters.
- Origin: on the ground directly below the midpoint between the two wheel axles.
- Blender: +X forward, +Z up, drivetrain on -Y.
- GLB / Three.js: +X forward, +Y up, drivetrain on +Z.
- Front and rear wheel pivot empties: x = ±0.524 m, height 0.357 m. Wheel meshes are centered on their axles. Rotate about local Y in Blender or local Z in standard glTF/Three.js after import (direction/sign depends on travel).
- Both tires touch ground at height zero.
- Assumed hood-center width 0.420 m; outside drop width about 0.489 m. Bag thickness 0.070 m. All three need measurement confirmation.
- Source studio ground, camera and lights are separate and excluded from GLB. No rock, gradient, shadow card or photograph is exported. The bicycle casts real shadows onto a separate scene surface.

## Validation

Exported GLB was independently parsed as glTF 2.0 with no external resource URIs. The deliverable was reimported successfully into Blender and rendered from both sides, straight front/rear and three-quarter. No source bicycle geometry remained in that reimport scene. Axles/wheels, opposite drivetrain placement and real front volume are visible in the five PNGs. This is a DCC reimport/render validation, not a mobile-browser performance benchmark or deployment test. The 22-mesh grouping reduces web draw overhead; further detailed-stage optimization remains possible.

The calm-motion reference site was treated only as a scene/interaction reference; no bicycle asset or geometry was copied from it. Browser behavior and lighting integration should be evaluated separately after the shape is approved.

## Needed before high-detail modeling

Please photograph this same Wichelsee build on a plain background, camera roughly at axle/frame height and far enough away to reduce wide-angle distortion:

1. Straight drivetrain side and straight opposite side, complete bicycle including tire contacts.
2. Straight front and rear, wheels aligned and handlebar level.
3. Front three-quarter and rear three-quarter, both sides if possible.
4. Close-ups of head-tube/fork junction, fork blades/mounts, hood and dropbar shape, saddle/seat clamp, bag sides/straps, both bottle cages/mini-pump and both sides of drivetrain/brakes.

Key measurements:

- Printed tire size or measured outside tire diameter, plus tire width.
- Axle-to-axle wheelbase.
- Handlebar width at hoods and drops; reach/drop or handlebar make/model if known.
- Frame size or geometry drawing (seat tube, effective top tube, head angle, stack/reach).
- Bag length, height and width, and rear/front hub spacing if exact depth matters.

Unresolved geometry: hidden-side cable routing, bag fabric/folds/back face, saddle underside, exact fork cross-sections/mount positions, actual drivetrain component models/tooth counts, rotor/caliper shapes and spoke pattern. Their present geometry is an explicit approximation. Please approve or correct the silhouette before high-detail modeling.

## File sizes

- RAIL_Wichelsee_blockout.blend: 4,357,488 bytes (4.16 MiB).
- RAIL_Wichelsee_blockout.glb: 1,274,488 bytes (1.22 MiB).
- 01_drivetrain_side.png: 2,600,041 bytes (2.48 MiB).
- 02_opposite_side.png: 2,582,538 bytes (2.46 MiB).
- 03_front.png: 1,807,492 bytes (1.72 MiB).
- 04_rear.png: 1,813,610 bytes (1.73 MiB).
- 05_three_quarter.png: 3,562,769 bytes (3.40 MiB).
- 06_primary_photo_comparison.png: 1,687,609 bytes (1.61 MiB).
