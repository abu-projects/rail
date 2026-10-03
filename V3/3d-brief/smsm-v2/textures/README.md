# Wichelsee v2 procedural PBR textures

Four restrained micro-surface sets, each 1024 × 1024 PNG. These are original procedural textures; the supplied side and front photographs informed color and material character only. All physical dimensions and colors below are visual estimates, not measurements or calibrated matches.

| Prefix | Base sRGB | Mean roughness | Estimated square tile |
|---|---|---:|---:|
| `nylon_black` | `#222527` | 0.85 | 64 mm |
| `rubber_black` | `#1b1d1d` | 0.80 | 40 mm |
| `tape_dark_chocolate` | `#4d3631` | 0.74 | 40 mm |
| `enamel_sage` | `#58765f` | 0.315 | 60 mm |

Each prefix supplies:
- `_basecolor.png`: RGB sRGB color; intentionally little contrast, no baked lighting.
- `_normal.png`: RGB linear, OpenGL/glTF tangent-space (+Y) normal map. Start at strength 1. The enamel can be reduced to 0.35–0.5 for distant shots.
- `_roughness.png`: grayscale linear roughness.
- `_orm.png`: RGB linear, R = 255 (neutral AO), G = roughness, B = 0 (nonmetal). Suitable for a glTF metallicRoughnessTexture.

Use repeat wrap in both UV directions, mipmapping and anisotropic filtering. With the image textures assigned, use white baseColorFactor, roughnessFactor = 1 and metallicFactor = 0. Do not multiply the roughness map by its listed mean again. For opaque enamel, metalness remains zero even though the tube below it is metal. Optional enamel clearcoat 0.15–0.25 with clearcoat roughness 0.2–0.3.

## UV examples

- Nylon bag: a roughly 500 × 120 mm panel spans 7.81 × 1.88 tile repeats; keep the weave aligned to the panel. Estimated yarn pitch is 0.5 mm. Build folds, zippers, binding and straps as mesh geometry.
- Tire rubber: roughly 54–56 repeats around a typical 700C gravel tire circumference. Use the same texture at normal strength 0.35 for sidewall rubber if useful. This surface does not specify or replace the tread-block pattern.
- Bar tape: 24 mm tape width spans 0.6 UV units. If the wrapping mesh already has seam edges, this map supplies only the fine surface. Avoid doubling its visual winding.
- Enamel: 60 mm tile; the near-uniform roughness variation and tiny orange-peel relief should become visible only under grazing highlights.

## Preview and validation

`pbr_tiled_preview.jpg` displays four 2 × 2 tiled patches; each patch compares base color to a simple normal-lit inspection. It is a presentation sheet, not a material map. `normal_inspection.png` shows the four normal maps together. Periodic generation and wrap gradients provide seamless edges; edge-change statistics are comparable to adjacent interior pixels (0.87–1.34× across the four normals). The material maps contain no fake logos, baked shadows, large folds or scratches.

`manifest.json` contains the machine-readable paths and settings. `generate_pbr.py` rebuilds all maps deterministically using Python, NumPy, SciPy and Pillow.
