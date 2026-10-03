# RAIL Wichelsee — 3D modeling handoff

## Send this prompt with the images in `references/`

Create a **real, fully three-dimensional, web-ready model** of the exact green RAIL Wichelsee gravel bicycle shown in the attached photos. This model will replace a flat image in an interactive website. Visitors must be able to see the bicycle from both sides, the front, the rear, and intermediate angles as it turns smoothly during scroll. Do not make a 2D cutout, billboard, shallow extrusion, or a generic bicycle with matching paint.

Use `01-wichelsee-main-side.jpg` as the primary reference for silhouette, proportions, components, and colors. `02-wichelsee-lineup-side.jpg` provides another side view and context; use only the green gravel bike at the upper right. `03-wichelsee-angle-group.jpg` and `04-wichelsee-front-group.jpg` provide partial perspective and front information; several other RAIL bikes are in those photos, so do not transfer their mountain-bike parts to Wichelsee. The existing website cutout and any promotional lighting are **not** geometry references.

Match the identifiable details: sage-green frame and tube junctions, black rigid fork, tan-wall gravel tires, black rims and spokes, drop handlebar with brown wrap, black frame bag and its straps, saddle and seatpost, crankset, rear cassette and derailleur, chain, disc brakes, bottle cages, cable routing, and correct asymmetry between drivetrain and non-drivetrain sides. Keep materials physically plausible with restrained roughness and metal response. Model the tire and wheel volume, frame depth, handlebars and bag so they hold up in a front view; no planar image tricks.

**First checkpoint:** make a blockout and send four orthographic or near-orthographic screenshots (drivetrain side, opposite side, front, rear), plus a three-quarter view. Identify geometry that cannot be determined from the supplied photos. Do not invent precise engineering measurements or claim a perfect reconstruction. Ask for the missing angles and key dimensions before high-detail modeling. Prioritize recognizability and clean silhouette over invisible mechanical detail.

**Final delivery:**

- Editable source project (`.blend` preferred; if another CAD/DCC tool is used, include its native project file).
- A genuine 3D `.glb`/glTF 2.0 export with embedded or supplied PBR textures, suitable for Three.js in a browser. A STEP file is welcome if parametric CAD was used, but it does not replace the GLB.
- Sensible real-world scale, bicycle centered around a documented origin, wheels touching a consistent ground plane, front direction and up-axis documented.
- Clearly named components/materials; wheels separate and centered on their axles if practical, so they can rotate independently.
- Optimized web version with no external missing textures, unnecessary hidden geometry, excessive subdivisions, or baked background/shadow. Include file size and approximate triangle count.
- Renders or screenshots from the five checkpoint angles, with a neutral studio light so shape and defects are visible.

The rock, gradient, lighting, and contact shadow belong to the website scene, **not** inside the bicycle model. The model itself must cast a correct, soft shadow on a separate surface under changing lights and camera angles. Test the exported GLB in a viewer from both sides and the front before delivery.

Visual interaction reference: https://cycle-3d.vercel.app/ — use it for the calm scroll/camera feel only; do not copy its bicycle design or assets.

## Reference images included

1. `references/01-wichelsee-main-side.jpg` — primary, highest-confidence side reference.
2. `references/02-wichelsee-lineup-side.jpg` — green gravel bicycle at upper right; comparison/context.
3. `references/03-wichelsee-angle-group.jpg` — green gravel bicycle at front/right of group; partial front and three-quarter clues.
4. `references/04-wichelsee-front-group.jpg` — green gravel bicycle at right of group; front width and handlebar clues. Other bicycles are different models.

## Additional inputs needed for high fidelity

Photograph this **same Wichelsee build**, ideally on a plain background and at a similar height: straight-on drivetrain side, straight-on opposite side, straight-on front, straight-on rear, front three-quarter, rear three-quarter, and a close-up of frame/fork/handlebar/bag. Provide tire size or measured wheel outside diameter, wheelbase, handlebar width, and frame size or geometry drawing if available. With only the attached images, the hidden side, exact depth, and some component shapes must be inferred.

## Review standard

Compare the blockout against `01-wichelsee-main-side.jpg` before detailing. Verify wheel diameters, axle positions, frame triangle, fork/head angle, handlebar and saddle silhouette, and bag outline. A front view must show actual volume; the opposite side must preserve bicycle asymmetry. After approval of that shape, proceed to materials and web optimization.
