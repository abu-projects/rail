# Client feedback photographs

Imported for “Railcycles.ch Feedback 1” (7 October 2026).

- `social/photo-1.png` through `photo-4.png`: the four attached photographs, mapped in the requested order to Instagram, Facebook, X and Tiktok. Buttons open local photographs, not social websites.
- `action/action-1.jpg` through `action-11.jpg`: originals from the action-photo folder linked in the email. Photographs 2, 5 and 11 are used on the homepage; the full set remains available for future selection. Existing photographer marks are preserved.

`python3 scripts/prepare-feedback-assets.py` (Pillow required) creates local WebP derivatives under `assets/feedback/`. `python3 scripts/build-site.py` regenerates the German and English pages. The approved root site is the implementation target.

The contact form currently prepares a local email draft. Direct server delivery requires a receiving service; no message is reported as sent by this site.
