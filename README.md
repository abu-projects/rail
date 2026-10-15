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

## Cloudflare Pages

Connect `abu-projects/rail`, select the `main` production branch, leave the framework preset as None, set the build command to `python3 scripts/build-cloudflare.py`, and set the output directory to `dist` (repository root as the build root).

The build regenerates the bilingual pages and packages the current site and its assets. Source photos, design documents, previews, and the V3 experiment are excluded. Cloudflare compiles `functions/` separately from the static `dist/` output. Commits to `main` trigger production deployments.
