# RAIL Cycles

This repository contains two static site versions:

- [Original site](https://abu-projects.github.io/rail/) — `index.html` at the repository root.
- [V3 3D home page](https://abu-projects.github.io/rail/V3/) — `V3/index.html`.

Both pages run from GitHub Pages without a build step. To preview locally, start a static HTTP server in this directory (for example `python3 -m http.server 4175`) and open `http://localhost:4175/` or `http://localhost:4175/V3/`. The V3 page loads its 3D model as a JavaScript module, so opening it via `file://` will not work reliably in browsers.

The editable Blender source, web GLB, texture masters, scripts, and delivery notes are kept in `V3/3d-brief/smsm-v2/`.

The bilingual pages are generated from `scripts/build-site.py` with `python3 scripts/build-site.py`. Feedback 3 workshop originals are in `imgs/Feedback-3/`, from the [supplied Drive folder](https://drive.google.com/drive/folders/1EtxuSPxYqwBBTRB3abs3uoBqTRdZnF0M). Regenerate their responsive WebP assets with `python3 scripts/prepare-workshop-assets.py` (requires Pillow).

The bilingual contact form posts to the Cloudflare Pages Function at `/api/contact`. It validates submissions on the server and sends through Resend. Success is displayed only when Resend accepts the email; errors preserve the visitor's entries. A hidden field filters simple bots, but is not a substitute for rate limiting or Turnstile if abuse occurs.

Set production variables in Cloudflare Pages before deploying:
- `RESEND_API_KEY`: encrypted secret, sending access restricted to `railcycles.ch`.
- `CONTACT_FROM_EMAIL`: `RAIL Cycles <website@railcycles.ch>` (verified Resend domain).
- `CONTACT_TO_EMAIL`: `tech@railcycles.ch`. This is the active Google Workspace mailbox shown in Wix; a live form test was delivered on 2026-10-15. The documented `sam@railcycles.ch` address bounced with Google SMTP 550 5.1.1.

To change the recipient, update `CONTACT_TO_EMAIL` and redeploy. Emails include a branded HTML layout, a plain-text fallback and the visitor’s Reply-To address. Visitor content is HTML-escaped. Never put API keys in Git or frontend code. Existing Google Workspace DNS records must remain in place; Resend is configured for sending only. Preview deployments remain unable to send unless explicitly configured.

Run backend checks with `node --test tests/contact.test.mjs`.

## Search, AI discovery and loading performance

`scripts/seo.py` generates unique German and English titles and descriptions,
absolute canonical URLs, reciprocal `de-CH`/`en`/`x-default` links, social previews,
and JSON-LD for the organization, website, pages, breadcrumbs and model catalogue.
Canonical URLs use the production origin `https://railcycles.ch` and Cloudflare
Pages' extensionless routes. Missing pages remain `noindex` and are excluded from
the sitemap. No review, stock status or exact purchase offer is invented for
custom frames.

The build writes `sitemap.xml` with all 14 public localized pages and `robots.txt`.
Public pages and assets are crawlable, including by OAI-SearchBot and other AI
search crawlers; `/api/` is excluded. Main content and model specifications are
available in HTML without JavaScript. An `llms.txt` file is not required for
Google's AI search features and does not guarantee inclusion or rankings.

Responsive AVIF photos are served with WebP fallbacks. The first hero image has
responsive preloads and high priority; additional hero slides load on demand.
Below-the-fold photos remain lazy-loaded, and generated image dimensions reserve
space. `_headers` enables bounded asset caching and long-lived caching for the
CSS/JS URLs whose query versions are derived from their contents. HTML is revalidated.
Run `python3 scripts/prepare-avif-assets.py` with Pillow/AVIF support after changing
original photos, then run the normal stdlib-only deployment build.

After deployment, submit `https://railcycles.ch/sitemap.xml` in the site's verified
Google Search Console and Bing Webmaster Tools properties. Inspect a German and
an English URL, and verify the live robots file and response headers. Cloudflare
WAF, bot challenges and zone-level AI crawler settings can override robots rules;
check those settings if legitimate crawlers receive challenges or 403 responses.
Do not disable general security protections. Local checks cannot confirm indexing,
real-user Core Web Vitals or a search ranking.

References: [Google AI search guidance](https://developers.google.com/search/docs/appearance/ai-features),
[OpenAI crawler controls](https://developers.openai.com/api/docs/bots),
[Cloudflare Pages headers](https://developers.cloudflare.com/pages/configuration/headers/).

## Cloudflare Pages

Connect `abu-projects/rail`, select the `main` production branch, leave the framework preset as None, set the build command to `python3 scripts/build-cloudflare.py`, and set the output directory to `dist` (repository root as the build root).

The build regenerates the bilingual pages and packages the current site and its assets. Source photos, design documents, previews, and the V3 experiment are excluded. Cloudflare compiles `functions/` separately from the static `dist/` output. Commits to `main` trigger production deployments.
