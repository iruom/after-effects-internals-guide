---
status: confirmed-local
evidence_grade: E2-L
versions: "24.5-era crash logs"
last_verified: 2026-09-14
---
# Advanced 3D crosses an Artisan/AEGP/BEE boundary

## Local evidence
One crash path contains `BEE_RenderTextureForArtisan`, `AEGPDriver`, `Advanced3D` plugin entry points, `PR_Render`, then BEE/RG checkout processing.

## Interpretation
Modern Advanced 3D is integrated through a host boundary descended from or compatible with AE's Artisan/AEGP architecture, while textures/layer results return into the BEE/RG compositing path.

## Caveat
This does not prove the Advanced 3D engine itself is implemented with the legacy Artisan sample architecture. It proves an observable integration boundary and naming continuity.

## Research target
Separate 3D scene rendering, layer-texture rendering, 2D compositing, color conversion and final RG composition by controlled 2D/3D mixed scenes.