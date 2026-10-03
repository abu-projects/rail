# RAIL Cycles

This repository contains two static site versions:

- [Original site](https://abu-projects.github.io/rail/) — `index.html` at the repository root.
- [V3 3D home page](https://abu-projects.github.io/rail/V3/) — `V3/index.html`.

Both pages run from GitHub Pages without a build step. To preview locally, start a static HTTP server in this directory (for example `python3 -m http.server 4175`) and open `http://localhost:4175/` or `http://localhost:4175/V3/`. The V3 page loads its 3D model as a JavaScript module, so opening it via `file://` will not work reliably in browsers.

The editable Blender source, web GLB, texture masters, scripts, and delivery notes are kept in `V3/3d-brief/smsm-v2/`.
