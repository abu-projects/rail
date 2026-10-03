# RAIL Cycles — V3 Design System

German Home · 3 October 2026

## Scope and sources

V3 is a separate Home concept. Its content source is the German `../index.html`. The earlier layout reference was [LOVIZ Cargo Bike](https://www.loviz.de/cargo-bike/); the current lighting and motion direction comes from [SPEACTRA Cycle 3D](https://cycle-3d.vercel.app/). The existing root site and `v2` remain separate.

Only Home is redesigned. Navigation, model details, contact and legal links lead to the existing German pages one directory above. All fonts, scripts, styles and images used by this Home live inside `V3`.

## Reference study

LOVIZ presents the bicycle as the continuous subject of the page. SPEACTRA adds a softly graded spotlight, a rocky plinth in the opening scene, a pronounced floor shadow in the next scene, and slow, continuous scroll transitions. Browser inspection of SPEACTRA found a full-size canvas marked `data-engine="three.js r185"`; its JavaScript loads a `bike.glb` model into Three.js. The visible rock is an ordinary `rock-pedestal.png` image, and the SVG elements are interface graphics. RAIL uses its own procedural Three.js bicycle rather than the reference model.

V3 translates these principles into RAIL:

| Reference principle | RAIL implementation |
| --- | --- |
| Product dominates the opening screen | A custom three-dimensional sage gravel bicycle above an original alpine-rock asset on a dark sage spotlight |
| Persistent product during scrolling | A viewport-pinned Wichelsee follows the whole Home journey, from the hero through the featured models, workshop, maker and contact sections |
| Short, large headings | Original RAIL headings, set in regular Barlow with deliberate line breaks |
| Minimal navigation | RAIL mark left; four German destinations and a DE indicator right |
| Large areas of empty space | Wide gutters, generous section spacing and a model gallery that changes sides with the bicycle |
| Product-led visual contrast | RAIL's monochrome UI, subdued sage illumination and the colors already present in its bicycles and workshop photography |
| Calm scroll movement | Frame-smoothed progress controls the bicycle's position, flip, scale, rock fade and floor-shadow reveal |

Neither reference site's logo, copy, bicycle assets or rock image is used. The references inform composition and pacing; RAIL retains its own identity and content.

## Design direction

Handmade bicycles, presented with the clarity of a softly lit product exhibition and the warmth of an actual workshop. The first viewport places Wichelsee on a low alpine rock under a sage spotlight. As the rock disappears, a dimly lit floor and contact shadow anchor the same bicycle beside the original model photographs. Workshop and portrait sections bring the maker into the story.

Avoid decorative dashboards, pill labels, invented specifications, pricing blocks, gradients on text and generic feature cards. Every section should serve the existing Home content. The reference's strong red color and technical-stat columns do not belong to RAIL's quieter identity.

## Color tokens

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#090C0A` | Main canvas |
| `--surface` | `#151B17` | Image loading surfaces |
| `--text` | `#F4F4F1` | Headings, logo, primary text; CTA background |
| `--muted` | `#B3BEB4` | Supporting text, eyebrows, secondary heading line |
| `--rule` | `#303A33` | Section rules and quiet separators |

CTA text uses `--bg` against `--text`. Hover uses `#D9D9D3`. Borders that must clearly read as controls use `#777777`. The stage gradient moves from charcoal through deep moss to restrained sage; it takes its cue from the Wichelsee frame rather than adding another brand color.

## Typography

Local Barlow WOFF2 files, with Arial/sans-serif fallback. Font files and their license are included under `assets/fonts/`. No external font request is required.

| Role | Desktop | Mobile | Weight / treatment |
| --- | --- | --- | --- |
| Opening heading | 72–116px | 60–94px, fluid | 400, line-height .99–1.01, tracking −.055em |
| Section heading | 42–88px | 42–62px | 400, line-height 1.04, tracking −.045em |
| Workshop heading | 54–110px | 57px | 400 |
| Contact heading | 66–158px | 76px | 400, tracking −.06em |
| Model name | 25–40px | 23–35px | 400, long words may wrap |
| Body | 18–19px | 17–18px | 400, line-height 1.55 |
| Navigation / links | 14–15px | 14–15px | 400–500 |
| Eyebrow | 12px | 10–12px | 500, uppercase, .13–.15em tracking |

The brand tagline “Built by Hand” stays as supplied in the source, including the English wording. The page language, navigation, sections and calls to action are German. There is no English version or language switch in this scope.

## Layout and spacing

- Content width: maximum 1440px with fluid 5.5vw side gutters, bounded by 24px and 96px.
- Header: 108px desktop, 88px mobile. Logo remains compact, 120–150px wide.
- Stage: full viewport on supported desktop screens; the opening copy transition spans 275svh. A separate sticky product layer is bounded by the entire Home page.
- Model gallery: on animated desktop, the first photograph is on the left and the bicycle occupies the right-hand lane. The next two photographs move to the right as the bicycle flips into the left-hand lane. Each model gets approximately one viewport of breathing room. Static layouts use two staggered columns on wider screens; mobile uses one column in source order.
- Main vertical spacing: approximately 130–180px desktop, 64–88px mobile.
- Workshop: full-bleed photograph with a dark overlay supporting text contrast.
- About: copy and small workshop detail on the left, Samuel's portrait in the middle, and the persistent product on the right. Mobile places the portrait after the copy and omits the decorative detail image.
- Contact: large two-line title and a circular arrow link, followed by a thin divider and structured footer.

## Home content map

| Section | Preserved source content |
| --- | --- |
| Hero | “RAIL Cycles · Sarnen, Schweiz”, “Built by Hand”, “Modelle entdecken”, “Entdecke RAIL” |
| Model introduction | “Ausgewählte Modelle”, “Vier Modelle. Eine Handschrift.”, “Von Gravel bis Trail. Vier Fahrräder, jedes mit seinem eigenen Namen.” |
| Featured model 1 | Trail · Muetterschwandenberg · “Modell ansehen” |
| Featured model 2 | Enduro Hardtail · Truischjanid · “Modell ansehen” |
| Featured model 3 | Gravel · Wichelsee · “Modell ansehen” |
| Model destination | “Alle Modelle entdecken” |
| Workshop | “Werkstatt”, “Hier entsteht dein RAIL.”, the original workshop paragraph, “Die Werkstatt entdecken” |
| Maker | “Über mich”, “Der Mensch hinter RAIL.”, “Samuel Kummrow. Der Mensch hinter RAIL Cycles.”, “Samuel kennenlernen” |
| Contact | “Lass uns über dein Bike sprechen.”, “Dein Weg zu RAIL.”, “Kontakt aufnehmen” |
| Footer | Original tagline, navigation, Samuel's address and email, copyright, legal links and “Nach oben” |

The root Home presents three featured entries under a heading mentioning four models. V3 preserves this choice rather than inventing an additional featured entry. The original slideshow controls are replaced by the new product-stage interaction; they are interface controls rather than editorial content.

## Motion and interaction

On supported desktop screens, one product layer remains pinned throughout the Home page rather than ending after the opening transition. “Built by Hand” fades upward and the model introduction appears on the left. The rock lowers and fades before the model gallery; a broad floor light and contact shadow take its place. Beside the first model, the bicycle sits on the right. During the scroll into the second model, the actual 3D geometry turns 180° around the vertical axis while travelling gradually into the left-hand lane; its front wheel points left when the move ends. It stays left beside the next photographs, then turns back to the right before the workshop. It sits over the workshop photograph, becomes a smaller third column beside Samuel's portrait, and grows again beside the contact call to action. It fades at the boundary with the footer. A one-pixel progress line marks the opening copy transition. Scroll direction naturally reverses every movement, including the turn.

The “Entdecke RAIL” anchor advances to the model introduction. “Alle Modelle entdecken” in that introduction moves to the featured photographs. The gallery's final link opens the existing model listing. Buttons and image links have restrained hover states; there is no autonomous carousel or continuous animation.

Implementation uses a passive scroll listener and a `requestAnimationFrame` loop that interpolates displayed scroll position toward actual scroll position. Transforms, 3D yaw and opacity are keyed to section positions. The Three.js scene is local to V3 and renders into a transparent WebGL canvas over the floor light and shadow. The 3D scroll composition is opt-in only when the viewport is at least 1024px wide and 670px high and reduced motion is not requested. Mobile, narrow tablets and short screens use normal document flow and the photographic cutout.

The desktop bicycle is a handcrafted geometric interpretation of the Wichelsee: tubes, wheels, spokes, tires, fork, saddle, bars, frame bag and drivetrain have depth and remain legible during rotation. It is not an exact product scan or engineering model. Reproducing the exact real bicycle from all angles would require a suitable CAD or photogrammetry GLB. The photographic cutout remains a fallback for mobile and browsers without WebGL.

## Accessibility and responsive behavior

- Semantic headings and landmarks; one H1, German `lang="de-CH"`.
- Skip-to-content link and visible keyboard focus.
- Hidden story panels become inert, preventing invisible links from capturing focus.
- Mobile navigation is a disclosure button with `aria-expanded` and `aria-controls`. Escape closes it and returns focus.
- No JavaScript: content and navigation remain in the document and visible.
- Reduced motion: sticky animation disabled; CSS animation and transitions disabled; anchors scroll without smoothing.
- Images have descriptive alt text; decorative imagery and arrows are hidden from assistive technology.
- Mobile layout uses normal page scrolling, stacked content and full-width model photographs.

## Assets and provenance

Original project assets copied into V3:

- `assets/rail.svg`: existing RAIL logo.
- `assets/fonts/`: existing local project fonts and license files.
- `assets/photos/`: original Muetterschwandenberg, Truischjanid, Wichelsee, workshop, workshop detail and Samuel photographs.

`assets/wichelsee-cutout.png` is an AI-assisted transparent product visualization created with the native `image_gen` tool from the existing `assets/home/wichelsee-800.webp` photograph. It is used in the mobile and WebGL-fallback layouts. The gallery retains the real original photographs. Generated extraction can reinterpret small components; it should not be treated as a technical product rendering.

`bike-3d.js` builds an original bicycle from Three.js primitives. The locally included `vendor/three.module.js` and `vendor/three.core.js` are Three.js r185, distributed under the MIT license in `vendor/LICENSE`. The scene does not request the reference site's GLB or any remote library.

`assets/alpine-rock.png` is a separately generated transparent stone prop, not a copy of the reference site. It sits behind the bicycle only in the opening scene and fades before the photographic model gallery. Built-in `image_gen` output, saved as a 1774 × 887 RGBA PNG.

Rock generation prompt (`transparent_background: true`):

> Use case: stylized-concept. Asset type: transparent foreground prop for RAIL Cycles German homepage hero. Generate ONLY a low, wide, rugged alpine rock pedestal, seen from a slightly elevated three-quarter frontal angle, capable of visually supporting a full side-view gravel bicycle. Dark charcoal slate and weathered gray stone, layered fractured geology, restrained realistic texture, premium product-photography lighting from above-left, soft subtle green-gray highlights. Composition: isolated rock occupying lower half of a wide landscape canvas with generous transparent empty space above, full edges visible, broad mostly level top, no ground plane. No bicycle, no wheels, no people, no text, no logo, no environment, no cast shadow outside the rock. Genuine alpha transparency everywhere outside the stone.

Generation prompt:

> Use case: background-extraction. Asset type: bicycle cutout for a dark RAIL Cycles website. Edit the supplied photograph: extract ONLY the actual green gravel bicycle, remove the entire building, shutter, concrete platform and all background. Preserve the photographed bicycle's exact geometry, side-view orientation, muted sage green paint, brown handlebar tape, tan tire sidewalls, black frame bag, saddle, silver bottle cage, drivetrain, thin spokes and all components. Do not redesign or add parts. Show the entire bicycle with both complete wheels, a small margin around it, centered and large in a landscape canvas. Transparent background everywhere around the bicycle and inside all gaps between the spokes and frame. No ground, no floor shadow, no annotations, no text, no graphic lines, no decorative items. A crisp clean faithful product cutout, not a new bicycle design.

Tool settings: source photograph supplied as `referenced_image_paths`; `transparent_background: true`. Saved asset: 1536 × 1024 PNG with alpha.

## Files and preview

```text
V3/
  DESIGN.md
  index.html
  home.css
  home.js
  bike-3d.js
  vendor/
    three.module.js
    three.core.js
    LICENSE
  assets/
    rail.svg
    wichelsee-cutout.png
    alpine-rock.png
    fonts/
    photos/
  previews/
```

Serve the project root with a static HTTP server, then open `/V3/`. The vendored Three.js modules need no package installation, build step, CDN or framework. Keep the parent German pages available for the outgoing navigation links.

## Verification

The original static and responsive layouts were reviewed in the Codex browser at 1440 × 900, 820 × 1180, 390 × 844 and 320 × 740. The current 3D stage was reviewed at 1440 × 900 through the hero and first three model transitions. At a quarter turn the geometry retains its depth rather than collapsing into an edge-on image. The mobile fallback and normal content flow were reviewed at 390 × 844. The bicycle stays visible throughout the main content and clears the footer.

The local reference audit checked 43 HTML references, CSS font paths and destination fragments: no missing targets. Seventeen key source-content checks passed. JavaScript syntax validation passed. Reduced-motion and no-JavaScript fallbacks were reviewed in the implementation; those browser preference modes were not separately emulated.

The `previews/` files document the initial V3 design before the continuous product-layer adjustment; the browser preview at `/V3/` shows the current version.
