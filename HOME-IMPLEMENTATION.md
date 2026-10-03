# RAIL — multipage website

Static German and English website. Serve this directory with `rtk python3 -m http.server 4173 --bind 127.0.0.1`, then open http://127.0.0.1:4173/.

## Pages and editing

- Five independent pages in each language: Home, Models, Workshop, About and Contact. German pages are at the root; English pages are under `en/`.
- Independent legal notice and privacy pages in both languages. All fourteen documents have real URLs, localized navigation and a language link to the equivalent page.
- The homepage is a concise gateway: cinematic hero, three featured model cards with individual model links and a view-all link, workshop and maker previews, and a contact invitation. Model details, workshop photographs and the maker profile live on their own pages.
- Edit copy, routes and shared HTML in `scripts/build-site.py`, and the hero template in `scripts/templates/home-hero.html`. Run `rtk python3 scripts/build-site.py` to regenerate HTML. Generated files can be served directly; no build tool is required at runtime.
- Shared presentation and behavior are in `home.css` and `home.js`.

## Content provenance and outstanding content

- Structure, model categories, photographs and contact information follow the two supplied client Word documents.
- Model-artwork spellings remain provisional: Muetterschwandenberg, Truischjanid, Wichelsee and Lopper. Categories are Trail, Enduro Hardtail, Gravel and Trail.
- Technical model descriptions, frame highlights, full workshop copy and full biography have not been supplied. Short introductory copy is proposed for client review; specifications and biography details have not been invented.
- The legal notice uses supplied business contact information. Privacy is visibly labelled as a draft: final hosting, email provider, recipients and retention details must be confirmed before publication. The briefing mentions Wix, but actual production hosting is not yet confirmed.
- This implementation has no analytics, advertising scripts, cookies, embedded maps or external font requests. The contact form collects name, email, optional model and message, validates required fields and email format, then prepares a local email draft with a copy fallback. It does not claim the message was sent. Contact links open the visitor’s email application; direct form delivery requires a provider/backend. The submit button stays disabled without JavaScript, with a direct-email fallback.
- `DESIGN.md` and unrelated research files were not changed. Nothing has been deployed.

## Assets and behavior

- Original photographs and `rail.svg` are preserved. `assets/rail-transparent.svg` removes only the logo’s black plate and is used in the header and footer.
- Responsive WebP derivatives are in `assets/home/`; original model wordmarks come from the layout DOCX. Fjalla One and Barlow are self-hosted with their OFL licenses in `assets/fonts/`.
- Header and logo remain fixed while scrolling; a dark header surface keeps navigation readable below the hero. Active-page state and the DE / EN bar appear on every page.
- The homepage preserves slow camera-style push-in, pull-out and lateral drift: 20-second alternating paths, 14-second holds and 2.4-second crossfades. Pause/resume affects camera movement and automatic slides. Manual navigation preserves playback choice. Hidden tabs, an offscreen hero and the mobile menu suspend motion. Reduced-motion preferences disable camera movement, autoplay and transitions.
- Mobile navigation supports Escape, focus containment and background inertness. All pages work as document navigation without JavaScript; navigation stays visible and the first hero image remains visible.
- Model enquiries lead to Contact with a whitelisted model selection prefilled in the form and a localized email subject. Switching language retains the selected model.

## Validation — 2 October 2026

- JavaScript syntax check passed.
- All fourteen generated documents checked for local asset/link/fragment resolution, unique IDs and one main heading.
- Browser checks covered independent page navigation, both language directions, model enquiry preservation, mobile menu navigation and legal links.
- Layout inspected at 320, 390 and 768 pixels and the desktop viewport. No horizontal overflow was observed on the checked mobile layouts. Scrolling confirmed the header remains at the top.
- Hero camera animation remains active with its 20-second timing. Prior motion verification covered pause/resume, manual navigation and crossfades; the multipage update retained that implementation.
- Browser console reported no warnings or errors during the multipage checks.
- Reduced-motion and no-JavaScript fallbacks were code-reviewed, not separately emulated in this round.
- Review screenshots are saved in `previews/multipage-home.png` and `previews/multipage-about.png`.

## Homepage and contact update

- Verified three featured model links, view-all, workshop, maker and contact destinations.
- Browser verified empty-field and invalid-email validation, encoded email draft, hiding an outdated draft after editing, English labels and model preselection. No email was sent.
- Homepage and contact form inspected at 390px without horizontal overflow. JavaScript syntax and all fourteen documents passed link/asset/fragment checks.
- New review screenshots: `previews/home-featured.png` and `previews/contact-form.png`.
