# RAIL Cycles — Design Direction

> A photographic, monochrome website about bicycles and the person who builds them.
> Large real photographs, condensed headings, generous black space, and direct German copy.

**Version:** 1.0 · **Reference reviewed:** 2 October 2026  
**Status:** Proposed implementation direction, grounded in the supplied brief, layout, photography, and logo. This is a design specification, not a finished website or approved final copy.

## 1. Project boundaries

- Build with static HTML, CSS, and small amounts of JavaScript.
- Complete the German website first. Begin English only after the German version is final; do not display an inactive language switcher.
- Five main pages: Home, Modelle, Werkstatt, Über mich, Kontakt. Impressum and Datenschutz are supporting pages.
- Use the existing RAIL identity and supplied photographs. The brief explicitly requests photographs rather than video.
- The home layout requests a rotating photographic hero with the words **“Built by Hand”** clearly visible.
- The purpose is to introduce RAIL, present four models, show the workshop and maker, and make contact easy. Shopping, accounts, checkout, a configurator, and a newsletter are outside the supplied scope.
- Treat the Word layout as the content and image guide. Use the reference for visual language and hierarchy; adapt both to the actual RAIL assets.

**Decision priority:** Current user decisions → supplied brand assets and brief → supplied layout → this specification → reference details. Generic design recipes must not override the real logo, requested image overlay, or German content.

## 2. Reference study: what transfers to RAIL

The [REEB homepage](https://reebcycles.com/) was inspected visually at desktop size and at a 390 × 844 mobile viewport. Its live rendered typography was also inspected. These observations describe the reference; subsequent sections specify new RAIL decisions.

| Observed pattern | RAIL adaptation |
| --- | --- |
| Black canvas, white type, colorful photography | Keep a monochrome interface; let RAIL bicycles and workshop light provide color. |
| Immersive workshop video and overlaid navigation | Use the requested photo sequence with a clearly readable logo and heading. |
| Tall, condensed capitals with conspicuous tracking | Keep the condensed character; reduce tracking for long German names. |
| Image-led two- and three-column groups | Use a consistent two-column overview for four models, preserving portrait photographs. |
| Outlined, slanted calls to action | Retain the outline contrast; use straight, precise rectangular RAIL buttons. |
| Craft story combining text and overlapping pictures | Use a calmer asymmetrical workshop composition with real process images. |
| Mobile menu becomes a dark side drawer | Use a simpler full-width menu with four main destinations. |

The [SST page](https://reebcycles.com/collections/sst) adds a useful sequence: large imagery, model introduction, construction details, then frame highlights. RAIL can use this hierarchy within its single Modelle page. Geometry tables, configurations, and technical claims require actual RAIL data and are not inherited.

The [About page](https://reebcycles.com/pages/about-us) puts real people behind the product. RAIL should make Samuel the focus of Über mich. The [Contact page](https://reebcycles.com/pages/contact) makes conversation a clear next step; RAIL can do this with its supplied email and address.

### Measured typography versus proposed values

| Property | Observed on REEB desktop | RAIL decision |
| --- | --- | --- |
| Display family | Fjalla One, weight 400 | Fjalla One, weight 400 |
| Body family | Barlow, weight 500 | Barlow, 400 for paragraphs; 500/600 for labels |
| Hero heading | 80px / 96px, 12px tracking | Fluid 48–96px, tighter line height and tracking |
| Body | 18px / 25.2px, 0.9px tracking | 18px / 28.8px, normal tracking |

The measured values are evidence, not tokens to copy verbatim. RAIL needs more comfortable reading and better handling of German words. The inspected desktop navigation also wrapped at approximately 1265px; RAIL's shorter navigation should stay on one line or switch to its mobile layout.

## 3. Brand character and color

The desired character is **hands-on, precise, personal, and outdoors-oriented**. The photographs already provide a credible workshop setting. Avoid decorative grunge, fake metal textures, generic outdoor stock photography, and artificially polished product renders.

### Confirmed brand evidence

`rail.svg` contains white artwork (`#FFFFFF`) on a black filled plate (`#000000`, the SVG's default fill). No chromatic brand accent is established by this asset. The neutral shades below are proposed interface colors, not additional official brand colors.

| Token | Value | Role |
| --- | --- | --- |
| `--color-brand-black` | `#000000` | Logo plate, navigation, hero text backing, footer |
| `--color-brand-white` | `#FFFFFF` | Logo artwork, key headings, primary CTA fill |
| `--color-bg` | `#0B0B0B` | Main page canvas; visually close to the reference black |
| `--color-surface` | `#171717` | Occasional alternate section or menu surface |
| `--color-text` | `#F4F4F1` | Main paragraph text |
| `--color-text-muted` | `#B8B8B2` | Captions and secondary information |
| `--color-rule` | `#393939` | Decorative separators; never the sole control boundary |
| `--color-control-border` | `#909090` | Visible outline buttons and control boundaries |
| `--color-on-light` | `#0B0B0B` | Text on the white primary button |
| `--color-focus` | `#FFFFFF` | Keyboard focus ring with a black separation layer |

**Color allocation:** The interface is black, white, and neutral gray. Green frames, warm timber, welding light, and concrete enter through photographs. Do not extract one bicycle's paint color and present it as RAIL's universal brand color. Do not import REEB's tan action color.

Calculated solid-color contrast: main text on the page canvas **17.86:1**; muted text on the alternate surface **9.00:1**; control outlines on that surface **5.62:1**; dark text on white **19.68:1**. Photograph overlays still require separate visual and contrast checks for each crop.

### Logo treatment

- Use the supplied SVG as an image, preserving its original artwork and `292.4 × 77.6` viewBox (approximately 3.77:1).
- Starting rendered width: 188px desktop, 152px mobile. Preserve aspect ratio with an automatic height.
- Keep at least 12px clear space around the asset at header size; no additional brand text should collide with it.
- The black plate is part of the file. It will be visible over a photograph and blend into a black header. Do not mistake it for export damage or apply a white fill to every path.
- No CSS inversion, stretching, glow, tint, or re-typesetting of the wordmark.
- Prefer external `<img>` usage so Illustrator's generic `.st0` and `.st1` classes cannot collide with site CSS.
- A standalone transparent mark or favicon would be a separate derived export if needed later. Preserve the original file.
- Keep model-logo spelling and proportions intact. Readability takes precedence over fitting a logo into a narrow card.

## 4. Typography

Use [Fjalla One](https://fonts.google.com/specimen/Fjalla+One) for strong display text and [Barlow](https://fonts.google.com/specimen/Barlow) for readable body text. The pair intentionally retains the reference's industrial character. Use local WOFF2 font files when implementing and retain their distributed license files; no font assets have been added at this documentation stage.

| Role | Family / weight | Size | Line height | Letter spacing |
| --- | --- | --- | --- | --- |
| Home hero | Fjalla One / 400 | `clamp(3rem, 6.5vw, 6rem)` | 1.06 | `0.035em` |
| Page title | Fjalla One / 400 | `clamp(2.5rem, 5vw, 4.5rem)` | 1.1 | `0.025em` |
| Section heading | Fjalla One / 400 | `clamp(2rem, 3.2vw, 3rem)` | 1.15 | `0.025em` |
| Model title | Fjalla One / 400 | `clamp(1.5rem, 2.5vw, 2.25rem)` | 1.2 | `0.01em` |
| Intro paragraph | Barlow / 400 | 20px desktop; 18px mobile | 1.5 | normal |
| Body / specifications | Barlow / 400 | 18px desktop; 17px mobile | 1.6 | normal |
| Navigation / buttons | Barlow / 600 | 14px | 1.2 | `0.08em` |
| Eyebrow / caption | Barlow / 500 | 13px | 1.45 | `0.06em` / normal |

- Uppercase is for short display headings, navigation, and button labels. Keep paragraphs in normal sentence case.
- Keep body copy between 45 and 65 characters per line; target `max-width: 60ch`.
- Use left-aligned paragraphs. Center only short section introductions or compact overview labels.
- Do not spread out German compound words with the reference's large letter spacing.
- Long model names must wrap without being clipped. Use approved editorial break points where appropriate; do not insert spelling changes, arbitrarily shrink the whole interface, or force `white-space: nowrap`.
- If a supplied model wordmark is used visually, retain a semantic text heading for accessibility. The image can be decorative when its exact name is already conveyed in text.
- Verify German umlauts and Swiss spelling in the actual font subset. Use `lang="de-CH"`; Swiss German orthography is the proposed editorial convention for this Swiss business.

## 5. Layout system

The structure should feel like a bicycle maker's photographic portfolio. Give each section one clear subject and enough black space to separate it from the next.

| Layout token | Desktop ≥ 1024px | Tablet 768–1023px | Mobile < 768px |
| --- | --- | --- | --- |
| Main content maximum width | 1360px | Available width | Available width |
| Minimum side gutter | 48px | 32px | 20px; 16px at ≤ 360px |
| Main grid | 12 columns | 8 columns | 4 columns |
| Column gap | 32px | 24px | 20px |
| Major section spacing | 112px | 80px | 64px |
| Within-section spacing | 40–48px | 32px | 24–32px |
| Header height | 88px | 80px | 72px |
| Minimum interactive target | 44 × 44px | 44 × 44px | 44 × 44px |

Use an 8px spacing rhythm, with 4px for fine alignment. Sections share one content edge. Full-width hero photography may extend beyond the content container; text always returns to the gutter.

Prefer square corners for buttons and image frames. The original rounded logo plate is a brand exception, not a reason to turn every component into a rounded card. Separate content with space, an occasional rule, or a change of surface. Avoid drop shadows and nested panels.

**Responsive principle:** Change composition before making text or images too small. Two model columns become one below 768px. Split stories stack with the image and associated text adjacent. Do not reverse the reading order using CSS in a way that differs from keyboard or screen-reader order.

## 6. Page structure and visitor journey

Primary navigation order: **Modelle · Werkstatt · Über mich · Kontakt**. The logo returns to Home. Contact is present even though the rough header sketch omits it, because it is a required page in the brief.

### Home

1. **Photographic hero:** RAIL logo and navigation; “Built by Hand”; one primary link, “Modelle entdecken”. Treat the English headline as the explicit exception supplied in the German layout, not as permission to mix languages elsewhere.
2. **Four-model overview:** A short “Unsere Modelle” heading and a two-by-two layout. Show the actual bike, its supplied name/wordmark, and “Modell ansehen”. Link to its section on Modelle. Keep descriptive copy short and factual once supplied.
3. **Workshop introduction:** Asymmetrical desktop split, approximately 7 columns image / 5 columns copy. Use a real making photograph, “Werkstatt”, a short approved paragraph, and “Einblick in die Werkstatt”.
4. **Maker introduction:** One portrait or Samuel with the bicycles, “Über mich”, a short approved introduction, and “Mehr über Samuel”. A smaller image than the hero creates a quieter reading moment.
5. **Contact invitation:** A brief approved heading, the visible email address, and “Kontakt aufnehmen”.
6. **Footer:** Logo, primary destinations, contact information, Impressum, Datenschutz.

This sequence follows product → process → person → conversation. Do not repeat a second complete catalogue lower down the same page.

### Modelle

- Start with the page title and four simple jump links. All four models must be discoverable without a carousel or filter.
- Present four complete sections in the supplied layout order: **muetterschwandenberg → truischjanid → wichelsee → lopper**. Spellings are provisional pending the reconciliation in §11.
- Each section contains its wordmark/name, complete bicycle photograph, approved description, frame highlights, and a “Modell anfragen” link to contact.
- Desktop detail composition: portrait image occupying approximately 5 columns; information occupying 6 columns; one column of breathing room. Keep a consistent side placement across the four sections for comparison.
- Mobile order: name → image → description → frame highlights → enquiry link.
- The Word layout reserves five frame-highlight items per model. Reserve content slots during development; never publish `Tbd`, invented specifications, geometry, prices, availability, or copied REEB claims.
- Use a semantic list for highlights; use a definition list if the supplied content becomes genuine label/value specifications.
- One Modelle page with anchors is sufficient for the supplied five-page scope. Separate model pages are a later content decision, not a prerequisite.

### Werkstatt

Begin with a large establishing workshop photograph and the title. Follow with a text introduction, then an edited sequence of two or three process images: frame alignment, welding, and close work. Alternate wide and portrait views deliberately. Captions describe visible actions only; process claims await Samuel's copy. End with a contact link.

### Über mich

Introduce Samuel with one strong portrait and his approved first-person story. Follow with a wider photograph connecting him to the bikes and workshop. Keep the tone personal and specific. Do not invent years of experience, certifications, company history, team members, or testimonials.

### Kontakt

Use a straightforward text-led layout with a supporting workshop or portrait image. Render the supplied details as selectable HTML, not text embedded in an image:

```text
Samuel Kummrow
St. Antoniastrasse 17
6060 Sarnen
Schweiz
sam@railcycles.ch
railcycles.ch
```

The email is visible and linked with `mailto:`. No form backend is specified; do not display a form that pretends to send a message. Add a form only when its delivery mechanism and states are part of the implementation scope. Do not invent opening hours or a phone number.

### Supporting legal pages

Impressum and Datenschutz use the same header/footer with a narrow, readable content column and clear heading hierarchy. Their final content is outstanding. Cookie/consent requirements depend on the actual services deployed and need review then; the design does not assume a banner or claim that none is needed.

## 7. Photography and source-asset map

All paths below are relative to the repository root. Originals remain unchanged. The images are high-resolution source material, not web-ready delivery sizes.

| Intended placement | Existing source | Direction |
| --- | --- | --- |
| Home hero, first slide | `imgs/Home/Rail_2025__LineUp_-59.jpg` | The image already used in the supplied home layout; broad lineup and architecture. |
| Home hero, second slide | `imgs/Home/Rail_2025__LineUp_-86.jpg` | Closer colorful group view; test text legibility against spokes and frames. |
| Home hero, third slide | `imgs/Home/Lopper.jpg` | Monochrome side-on bicycle; maintain the existing photographic treatment. |
| Mobile hero alternate candidate | `imgs/Home/Rail_2025__LineUp_-84.jpg` | Native portrait composition; use art direction if the wide source cannot preserve its subject. |
| muetterschwandenberg | `imgs/Rubrik Modelle/Modell Mutterschwandenberg Fully.jpg` | Green full-suspension bicycle; original portrait framing. |
| truischjanid | `imgs/Rubrik Modelle/Modell Truise Enduro Hardtail.jpg` | Dark hardtail; original portrait framing. |
| wichelsee | `imgs/Rubrik Modelle/Modell Wichselsee Gravel.jpg` | Green gravel bicycle; original portrait framing. |
| lopper | `imgs/Rubrik Modelle/Modell Lopper Fully.jpg` | White full-suspension bicycle; original portrait framing. |
| Home workshop teaser | `imgs/Rubrik Werkstatt/TruschJaNid_2022_-100.jpg` | Wide workbench scene showing the maker at work. |
| Workshop establishing image | `imgs/Rubrik Werkstatt/TruschJaNid_2022_-44.jpg` | Wide overview of the actual workshop. |
| Workshop process | `imgs/Rubrik Werkstatt/TruschJaNid_2022_-8.jpg` | Frame handling/alignment; keeps attention on the craft. |
| Workshop close view | `imgs/Rubrik Werkstatt/TruschJaNid_2022_-12.jpg` | Portrait detail; pair with text rather than stretching to a banner. |
| Home maker teaser | `imgs/Rubrik über mich/Rail_2025__LineUp_-60.jpg` | Samuel with the four bikes; landscape composition. |
| About lead portrait | `imgs/Rubrik über mich/Rail_2025__LineUp_-90.jpg` | Monochrome portrait with bicycle. |
| About secondary image | `imgs/Rubrik über mich/Rail_2025__LineUp_-56.jpg` | Wider, quieter architectural scene. |
| Main identity | `rail.svg` | Preserve the supplied black plate and white artwork. |
| Model identity source | `imgs/Logo Design/Rail Frame Sticker - Model.eps` | Export individual web assets later; do not place the entire sticker sheet on a page. |

The `über mich` source directory uses a decomposed Unicode umlaut. Resolve actual filenames during asset preparation rather than retyping visually identical paths. Web derivatives can use simple ASCII names with an explicit mapping to their originals.

### Cropping rules

- Product identity images retain the entire frame and both wheels. Default to their native 2:3 portrait ratio with `width: 100%; height: auto`.
- The source portraits contain substantial architecture around the bicycles. In the overview, display them generously—approximately 420–500px wide on desktop—rather than squeezing four thumbnails into one row.
- Do not force the portraits into a 16:9 `object-fit: cover` slot. A tighter manual derivative can be explored later only after checking the complete bike remains visible.
- Wide workshop photographs can use 3:2 or 16:10 frames. Portraits remain 2:3 or an individually checked 4:5 crop.
- Use full-width `cover` only for atmospheric hero images with tested focal points. Do not assume `50% 50%` works for every image and viewport.
- Preserve existing color and monochrome treatments. Do not apply a global desaturation filter or a green brand tint.
- Never put a heading across Samuel's face or the central bicycle frame. Prefer a quiet area; use a localized gradient or separate text block when needed.

## 8. Hero and component behavior

### Hero slideshow

- Desktop starting height: `clamp(560px, 82svh, 880px)`. Text is near the lower left with 48–64px bottom clearance, within the common content gutter.
- Mobile starting composition: approximately 62–72svh of image, bounded sensibly for short screens. Allow the text region to grow; never clip the CTA to preserve a fixed height.
- Use the first source image from the supplied layout on desktop. On mobile, choose a tested crop or the specified portrait alternative; do not lose all four bikes merely to fill the screen.
- Keep “Built by Hand” as real HTML text. Place it over a quiet, darkened region. A starting overlay is a black gradient from about 65% opacity at the lower edge to transparent through the upper half, plus a subtle top backing for navigation. This is a starting treatment, not a guaranteed contrast result.
- If the mobile crop cannot accommodate readable text, position the title/CTA in a black block immediately adjoining the photograph. Preserve the image rather than increasing the overlay until it is barely visible.
- Three slides are enough initially. Change images every 7 seconds with a 500ms crossfade. Keep the heading and CTA stationary.
- Provide previous/next buttons, a visible pause/resume control, and a textual slide count. Controls have accessible German names and 44px hit areas.
- Pause while keyboard focus is within the hero and on pointer hover; after explicit pause or manual navigation, require explicit resume. Do not continually announce automatic slide changes to screen readers.
- With reduced motion enabled, do not autoplay; show the first image and allow instantaneous manual changes. With JavaScript unavailable, show the first image, heading, and working link.

### Header and mobile navigation

- On Home, overlay the hero with sufficient dark backing for legibility. Interior pages use a solid black header.
- A sticky header may become solid after leaving the top; keep its height stable to avoid a visible jump.
- Use a visible underline for the active page plus `aria-current="page"`.
- Switch to the mobile menu below 1024px. Four large navigation links are sufficient; no multi-level ecommerce drawer is needed.
- Mobile menu: opaque black full-width panel, close control, clear separators, current-page state. Support Escape, manage focus, restore focus to the trigger, and prevent interaction with the covered page.
- Keep navigation usable without JavaScript, for example by enhancing an initially visible navigation block.

### Calls to action and links

| Component | Resting appearance | Interaction |
| --- | --- | --- |
| Primary CTA | White fill, black text, 1px white border | Light gray hover; visible outlined focus |
| Secondary CTA | Transparent fill, white text, `--color-control-border` outline | White fill and black text on hover/focus |
| Text link | Underlined in paragraph copy | Brighter underline; no dependence on color alone |
| Model image link | No enclosing card shell | Optional scale up to 1.02 inside an overflow-hidden image wrapper |

Buttons start at 48px high with 24px horizontal padding. Allow German labels to wrap if required. Keep text upright, corners square, and focus rings outside any clipped media wrapper. Use links for navigation and buttons for actions.

### Footer

Use a black surface and one quiet separator. Desktop: logo, navigation, and contact in three aligned groups. Mobile: stack those groups and keep legal links visible. Do not import the reference's newsletter, shopping links, social accounts, or large decorative ghost logo without real RAIL content and a reason.

## 9. Motion, accessibility, and delivery

Motion supports the photographs without competing with them. Use 160–220ms for hover/focus transitions and 220–280ms for the menu. Optional section reveals are limited to opacity and 12px translation over roughly 350ms, once only. Content must remain visible if the enhancement fails. No scroll hijacking, continuous marquees, custom cursor, parallax, or perpetual decoration.

Accessibility requirements for implementation:

- One clear `h1` per page; subsequent headings reflect the content hierarchy.
- A visible-on-focus skip link, semantic navigation, main content, and footer.
- All essential content and destinations available without hover or dragging.
- At least 4.5:1 text contrast for normal text and 3:1 for large text; verify hero text against every actual image/crop. These are implementation acceptance criteria, not a completed compliance audit.
- A two-layer focus treatment: white ring with black separation, so focus remains visible over both bright and dark images.
- Informative German alt text for meaningful photographs. Avoid claiming model specifications from the picture. Decorative duplicate images use empty alt text.
- Verify at 320px width, enlarged text, keyboard-only navigation, and reduced motion. No horizontal page overflow, clipped model names, or inaccessible slideshow controls.

Delivery targets, to be measured when the site exists:

- Generate responsive AVIF/WebP derivatives with a suitable fallback; preserve original sources.
- Suggested widths: 480, 800, 1200, 1600, and 2000px as appropriate to the image role. Do not generate every size for every image mechanically.
- Aim for a first hero image around 200–400KB at the relevant delivery size, increasing only where visual quality requires it. Do not serve the original multi-megabyte photograph by default.
- Load the first hero image eagerly with dimensions and high priority; lazy-load below-the-fold images. Do not eagerly download the entire slideshow at every available resolution.
- Explicit image dimensions or aspect ratios prevent layout movement. Use `srcset` and `sizes` based on actual layout slots.
- Self-host the chosen font files, use `font-display: swap`, and load only the required weights and glyph sets.
- Keep navigation and content in ordinary HTML. A heavy application framework or carousel dependency is unnecessary for this scope.

## 10. German interface copy

These short labels are implementation proposals. Descriptive and promotional paragraphs still require final content.

| Purpose | Label |
| --- | --- |
| Hero heading, supplied exception | Built by Hand |
| Hero action | Modelle entdecken |
| Overview heading | Unsere Modelle |
| Model overview action | Modell ansehen |
| Frame-detail heading | Rahmendetails |
| Model enquiry | Modell anfragen |
| Workshop action | Einblick in die Werkstatt |
| About action | Mehr über Samuel |
| Contact action | Kontakt aufnehmen |
| Open / close menu | Menü öffnen / Menü schliessen |
| Slideshow controls | Vorheriges Bild / Nächstes Bild |
| Slideshow playback | Diashow pausieren / Diashow fortsetzen |

“Rahmendetails” is the proposed German equivalent of the layout's “Frame Highlights”; this label can be adjusted during copy review. Brand/model names remain unchanged. Do not add unverified marketing language such as lifetime guarantees, local sourcing, award claims, or bespoke production promises.

## 11. Content decisions still open

These items do not block visual design. Resolve them before treating the affected content as final.

| Item | Evidence / next decision |
| --- | --- |
| Model names | The brief uses “Wicheslsee”, “Truise”, and “Mutterschwandenberg”; filenames use other variants. Supplied model artwork reads “wichelsee”, “truischjanid”, and “muetterschwandenberg”. Use artwork spellings provisionally and ask for final editorial confirmation. |
| Model categories | The brief calls Lopper and Mutterschwandenberg “Trail”; file names call them “Fully”. Confirm final labels rather than guessing from the photos. |
| Model descriptions and highlights | Four descriptions and the five intended highlight items per model are outstanding. |
| Workshop and biography | The layout explicitly says text will follow. Use its intended space while developing; do not publish filler copy. |
| Legal content and consent | Final text and deployed services need review. No legal conclusion is made by this design document. |
| Hosting | The brief mentions Wix; the user chose static HTML. Actual deployment destination and domain configuration are separate implementation decisions. |
| English | Deferred until the German content and layout are final. Keep components reusable; do not maintain a second content version yet. |

## 12. Design acceptance checklist

- [ ] The first view unmistakably shows RAIL, a real RAIL image, “Built by Hand”, and a clear next action.
- [ ] The interface follows the neutral palette; photographic greens and warm workshop colors remain natural.
- [ ] The supplied SVG renders at its correct ratio with its black plate intact.
- [ ] All four bicycles appear complete, at a useful size, in the intended order.
- [ ] Desktop, tablet, and mobile compositions use the same visual hierarchy without squeezing the desktop layout into a narrow screen.
- [ ] Long names and German labels remain readable at 320, 390, 768, 1024, and 1440px widths.
- [ ] Navigation, model anchors, contact links, menu, and slideshow work with the keyboard.
- [ ] Each hero slide has a checked crop, readable text, and accessible playback controls.
- [ ] Reduced motion and no-JavaScript fallbacks keep content available.
- [ ] Images and fonts are delivered efficiently without visible layout shifts.
- [ ] Final content contains no `Tbd`, invented specifications, dead language toggle, or non-functional form.
- [ ] Impressum, Datenschutz, model naming, and supplied descriptive copy are resolved before launch.

## 13. Source record

Local sources reviewed: `Briefing Website Sam.docx`, `Layout Website Sam.docx`, the 28 photographs under `imgs/`, supplied EPS identity artwork, and the newly exported `rail.svg`.

External reference review: [REEB homepage](https://reebcycles.com/) and [SST model presentation](https://reebcycles.com/collections/sst) inspected in the browser; [About](https://reebcycles.com/pages/about-us) and [Contact](https://reebcycles.com/pages/contact) reviewed for content structure. Desktop and mobile observations are dated 2 October 2026, not a claim of exhaustive cross-browser testing. Font family pages: [Fjalla One](https://fonts.google.com/specimen/Fjalla+One), [Barlow](https://fonts.google.com/specimen/Barlow).

The supplied materials establish requirements and available assets. Exact spacing, neutral UI shades, responsive rules, component behavior, and asset placements in this document are RAIL design proposals. No reference images, commercial copy, theme code, or product specifications are part of the proposed site assets.
